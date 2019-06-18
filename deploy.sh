#!/bin/bash

rm function.zip
cd venv/lib/python3.7/site-packages/
zip -r9 ../../../../function.zip .
cd ../../../../
zip -g function.zip lambda_function.py
aws lambda update-function-code --function-name DrSherry --zip-file fileb://function.zip
