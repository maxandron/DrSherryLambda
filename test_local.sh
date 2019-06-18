#!/bin/bash

python-lambda-local -t 30 -f lambda_handler lambda_function.py events/add_task.json
