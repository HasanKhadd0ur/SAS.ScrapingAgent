from abc import ABC, abstractmethod
from typing import List

from app.core.models.credential_model import TelegramCredential

class BaseConfig(ABC):
    @abstractmethod
    def get_user_agents(self) -> List[str]:
        pass

    @abstractmethod
    def get_random_user_agent(self) -> str:
        pass
    def get_api_key(self)->(str,str):
        pass
    def get_config(self,key)->any:
        pass
    def get_random_telegram_credential(self) -> TelegramCredential:
        pass
    def get_master_url(self) -> str: 
        pass
    def get_scraper_name(self)-> str:
        pass
