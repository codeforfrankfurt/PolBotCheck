import os
db_credentials = {'protocol': 'http', 'host': os.environ['HOST'], 'port': int(os.environ['PORT']), 'username': os.environ['USERNAME'], 'password': os.environ['PASSWORD']}
