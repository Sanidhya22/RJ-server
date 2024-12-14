import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")

        # Check for critical environment variables
        required_env_vars = ["TELEGRAM_BOT_TOKEN"]
        for var in required_env_vars:
            if not os.environ.get(var):
                raise ValueError(f"Environment variable {var} is missing")
