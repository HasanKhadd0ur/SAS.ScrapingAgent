class CredentialsService:
    def __init__(self, db):
        self.collection = db["credentials"]

    def get_available_bot_token(self) -> str:
        token_doc = self.collection.find_one(
            {"type": "telegram_bot", "active": True},
            sort=[("priority", 1)]
        )
        if not token_doc:
            raise Exception("No active Telegram bot token available")
        return token_doc["token"]
