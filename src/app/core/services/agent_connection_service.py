import socket
import httpx

class AgentConnectionService:
    def __init__(self, master_url: str, scraper_name: str):
        self.master_url = master_url
        self.scraper_name = scraper_name
        self.scraper_id = None

    async def connect(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        payload = {
            "scraperName": self.scraper_name,
            "hostname": hostname,
            "ipAddress": ip_address
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.master_url}/api/scrapers/connect", json=payload)
            response.raise_for_status()
            self.scraper_id = response.json().get("value")
            print(f"Connected to master, scraper ID: {self.scraper_id}")
