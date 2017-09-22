from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

from analytics.flask_api_server import app

if __name__ == "__main__":
    app.run()
