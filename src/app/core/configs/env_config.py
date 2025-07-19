import os
import random
from typing import Dict, List

from dotenv import load_dotenv
from pymongo import MongoClient

from app.core.configs.base_config import BaseConfig
from app.core.models.credential_model import TelegramCredential

uri = "mongodb://localhost:27017"
mongo_db_name = "scrapers"
config_collection_name = "config"
credential_collection_name = "credentials"

class EnvSettings:
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client[mongo_db_name]
        self.config_collection = self.db[config_collection_name]
        self.credential_collection = self.db[credential_collection_name]

        self._configs_cache: Dict[str, dict] = {}

        # Load user agents from DB, fallback to empty list if not found
        try:
            self.user_agents: List[str] = self.get_config_from_db("USER_AGENTS")
        except KeyError:
            self.user_agents = []
            print("Warning: No USER_AGENTS config found in DB, using empty list.")

    def get_config_from_db(self, key: str) -> dict:
        if key in self._configs_cache:
            return self._configs_cache[key]
        
        result = self.config_collection.find_one({"key": key})
        if not result or "config" not in result:
            raise KeyError(f"No config found in DB for key: {key}")
                
        self._configs_cache[key] = result["config"]
        return result["config"]

    def get_all_telegram_credentials(self) -> List[TelegramCredential]:
        return [
            TelegramCredential.from_dict(doc)
            for doc in self.credential_collection.find({"type": "telegram", "active": True})
        ]
    def get_pipeline_config(self) -> dict:
        return self.get_config_from_db("PIPELINE_CONFIG")    

class EnvConfig(BaseConfig):
    def __init__(self):
        load_dotenv()
        self.settings = EnvSettings()
        self.telegram_credentials = self.settings.get_all_telegram_credentials()

    def get_user_agents(self) -> List[str]:
        return self.settings.user_agents

    def get_random_user_agent(self) -> str:
        return random.choice(self.settings.user_agents) if self.settings.user_agents else "default-user-agent"

    def get_api_key(self) -> str:
        api_id = os.getenv("API_ID")
        api_key = os.getenv("API_KEY")
        
        if not api_id or not api_key:
            raise EnvironmentError("API_ID or API_KEY environment variable is not set")
        return api_id, api_key

    def get_config(self, key: str) -> dict:
        return self.settings.get_config_from_db(key)
        
    def get_random_telegram_credential(self) -> TelegramCredential:
        if not self.telegram_credentials:
            raise ValueError("No active Telegram credentials found in DB.")
        return random.choice(self.telegram_credentials)

    def get_master_url(self) -> str: 
        return os.getenv("MASTER_URL", "http://localhost:5050")
    
    def get_scraper_name(self)-> str:
        return os.getenv("SCRAPER_NAME", "MyScraperAgent")
