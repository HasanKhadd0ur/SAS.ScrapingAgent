import socket
import httpx
import logging

class MasterConnectionService:
    def __init__(self, master_url: str, scraper_name: str):
        self.master_url = master_url
        self.scraper_name = scraper_name
        self.scraper_id = None
        self.logger = logging.getLogger(__name__)

    async def connect(self) -> int:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        payload = {
            "scraperName": self.scraper_name,
            "hostname": hostname,
            "ipAddress": ip_address
        }

        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(f"{self.master_url}/api/scrapers/connect", json=payload)
                response.raise_for_status()
                self.scraper_id = response.json()
                print(f"[INFO] Connected to master, scraper ID: {self.scraper_id}")
                self.logger.info(f"Connected to master, scraper ID: {self.scraper_id}")
                return  self.scraper_id
            
        except httpx.HTTPError as e:
            error_msg = f"[ERROR] Failed to connect to master: {str(e)}"
            print(error_msg)
            self.logger.error(error_msg)
