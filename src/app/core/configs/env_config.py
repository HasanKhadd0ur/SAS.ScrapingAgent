# app/config/env_config.py
import os
import random
from typing import List

from dotenv import load_dotenv
from pymongo import MongoClient

from app.core.configs.base_config import BaseConfig
from app.core.configs.scrapers_config import BASE_CONFIG, DUMMY_SCRAPER_CONFIG, TELEGRAM_WEB_SCRAPER_CONFIG

uri = "mongodb://localhost:27017"
mongo_db_name = "scraper"           # database name
mongo_collection_name = "config"  # collection name

class EnvSettings:
    def __init__(self):
        self.client = MongoClient(uri)
        self.db = self.client[mongo_db_name]
        self.collection = self.db[mongo_collection_name]
        self._configs_cache = {}

    user_agents: List[str] = [
        "EventLocationService/1.0 (dummy121@example.com)",
        "EventLocationService/1.0 (dummy2324@example.com)",
        "EventLocationService/1.0 (dummy342343@example.com)",
        "EventLocationService/1.0 (dummy4342@example.com)",
        "EventLocationService/1.0 (dummy324235@example.com)",
        "EventLocationService/1.0 (dummy63242@example.com)",
        "EventLocationService/1.0 (dummy72343@example.com)",
        "EventLocationService/1.0 (dummy83432@example.com)",
        "EventLocationService/1.0 (dummy9342@example.com)",
        "EventLocationService/1.0 (dummy13240@example.com)",
    ]

class EnvConfig(BaseConfig):
    def __init__(self):
        load_dotenv() 
        self.settings = EnvSettings()
        self._configs = {
            "BASE_CONFIG": BASE_CONFIG,
            "DUMMY_SCRAPER_CONFIG": DUMMY_SCRAPER_CONFIG,
            "TELEGRAM_WEB_SCRAPER_CONFIG": TELEGRAM_WEB_SCRAPER_CONFIG,
        }

    def get_user_agents(self) -> List[str]:
        return self.settings.user_agents

    def get_random_user_agent(self) -> str:
        return random.choice(self.settings.user_agents)
    
    def get_api_key(self) -> str:
        api_id = os.getenv("API_ID")
        api_key = os.getenv("API_KEY")
        
        if not api_key:
            raise EnvironmentError(" environment variable is not set")
        return api_id,api_key
    
    def get_config(self, key: str) -> dict:
        try:
            return self._configs[key]
        except KeyError:
            raise KeyError(f"No config found for key: {key}")