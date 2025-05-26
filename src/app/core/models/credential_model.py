from dataclasses import dataclass
from typing import Optional

@dataclass
class TelegramCredential:
    session_name: str
    auth_type: str 
    api_id: Optional[int] = None
    api_hash: Optional[str] = None
    bot_token: Optional[str] = None
    active: bool = True

    @staticmethod
    def from_dict(data: dict):
        return TelegramCredential(
            session_name=data.get("session_name"),
            auth_type=data.get("auth_type"),
            api_id=data.get("api_id"),
            api_hash=data.get("api_hash"),
            bot_token=data.get("bot_token"),
            active=data.get("active", True),
        )
