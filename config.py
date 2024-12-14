import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.redis_url = os.environ.get("REDIS_HOST")
        self.redis_password = os.environ.get("REDIS_PASSWORD")
        self.kite_api_key = os.environ.get("KITE_API_KEY")
        self.kite_secret = os.environ.get("KITE_SECRET")
        self.zerodha_id = os.environ.get("ZERODHA_USERID")
        self.zerodha_password = os.environ.get("ZERODHA_PASS")
        self.zerodha_totp = os.environ.get("ZERODHA_TOTP")
        self.telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.telegram_channel_id = os.environ.get("TELEGRAM_CHANNEL_ID")

        # Check for critical environment variables
        required_env_vars = ["REDIS_HOST",
                             "REDIS_PASSWORD", "KITE_API_KEY", "KITE_SECRET"]
        for var in required_env_vars:
            if not os.environ.get(var):
                raise ValueError(f"Environment variable {var} is missing")
