#!/bin/bash

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

if [[ "$FLASK_ENV" == "production" ]]; then
	export PYTHONPATH="./polbotcheck:./webapi"
	: ${WEB_CONCURRENCY:=4}
	export WEB_CONCURRENCY=$WEB_CONCURRENCY
	gunicorn -w $WEB_CONCURRENCY  --pythonpath $PYTHONPATH --log-file - wsgi:app
else
	export PYTHONPATH="../polbotcheck"
	python analytics/flask_api_server.py
fi
