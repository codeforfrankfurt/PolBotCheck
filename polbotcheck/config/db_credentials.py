import os

if not os.environ.get('FLASK_ENV') == 'production':
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override=True)

db_credentials = {'protocol': 'http', 'host': os.environ['DB_HOST'], 'port': int(os.environ['DB_PORT']), 'username': os.environ['DB_USERNAME'], 'password': os.environ['DB_PASSWORD']}
