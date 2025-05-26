from abc import ABC, abstractmethod
from typing import List

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
    