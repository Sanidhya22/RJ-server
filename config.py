import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.project_id = os.environ.get("project_id")
        self.private_key_id = os.environ.get("private_key_id")
        self.private_key = os.environ.get("private_key")
        self.client_email = os.environ.get("client_email")
        self.client_id = os.environ.get("client_id")
        self.client_x509_cert_url = os.environ.get("client_x509_cert_url")

        # Check for critical environment variables
        required_env_vars = ["TELEGRAM_BOT_TOKEN"]
        for var in required_env_vars:
            if not os.environ.get(var):
                raise ValueError(f"Environment variable {var} is missing")
