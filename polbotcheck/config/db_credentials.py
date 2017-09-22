import os
db_credentials = {'protocol': 'http', 'host': os.environ['DB_HOST'], 'port': int(os.environ['DB_PORT']), 'username': os.environ['DB_USERNAME'], 'password': os.environ['DB_PASSWORD']}
