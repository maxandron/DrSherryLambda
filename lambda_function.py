import json

from notion.client import NotionClient

DEBUG = True


def simple_google_response(tts):
    return {
        "payload": {
            "google": {
                "expectUserResponse": False,
                "richResponse": {
                    "items": [
                        {
                            "simpleResponse": {
                                "textToSpeech": "<speak>{}</speak>".format(tts)
                            }
                        }
                    ]
                }
            }
        }
    }


def debug_print(msg):
    if DEBUG:
        print(msg)


def add_notion_task(task_name):
    debug_print("Adding task {}".format(task_name))
    client = NotionClient(
        token_v2="xxx")
    cv = client.get_collection_view(
        "https://www.notion.so/maxandron/8490e16a3cff46c78653276418f52c3f?v=56bfbaf1144b497d9cdca0c12cfcb238")
    row = cv.collection.add_row()
    row.name = task_name
    # <break time=\"500ms\"/>
    return simple_google_response("I'll remind you to {}".format(task_name))


def done_response():
    return "consider it done"


def out_of_stock(grocery):
    client = NotionClient(
        token_v2="xxx")
    cv = client.get_collection_view(
        "https://www.notion.so/maxandron/c13b2e80461e4ff8aef6d97def004866?v=a1a072ebc1034da08fa5961c576368d0")

    for row in cv.collection.get_rows():
        if row.name == grocery:
            row.in_stock = False
            return simple_google_response(done_response())

    return simple_google_response("Grocery not found")


def response(body, err=200):
    res = {
        "isBase64Encoded": False,
        "statusCode": err,
        "headers": {},
        "body": json.dumps(body)
    }
    debug_print("Response {}".format(json.dumps(res)))
    return res


def lambda_handler(event, context):
    """Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.
    """
    if DEBUG:
        debug_print("Received event: " + json.dumps(event))
    body = event.get("body", event)
    if type(body) != dict:
        body = json.loads(body)

    action = body['queryResult']['intent']['displayName']
    parameters = body['queryResult']['parameters']

    if "add task" == action:
        return response(add_notion_task(parameters['task_name']))
    if "out of stock" == action:
        return response(out_of_stock(out_of_stock(parameters["grocery"])))

    return response("intent {} is not recognized".format(action), 400)
