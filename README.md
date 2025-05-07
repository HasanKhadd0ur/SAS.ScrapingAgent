# 🕷️ SAS.ScrapingAgent

**SAS.ScrapingAgent** is a scalable, modular scraping service that collects and processes real-time data from platforms like **Telegram**, **Nitter**, and others. It is part of a larger microservices-based system designed for monitoring and detecting local events such as crimes and disasters using social media content.

---

## 📦 Features

* 🔌 Supports multiple scraping sources (Telegram, Nitter, etc.)
* 📄 Extracts structured data
* 🎯 Pipeline for preprocessing and filtering
* ⚙️ Easily extendable with new scraper modules
* 🛠 Uses **Selenium** or **Playwright** for web scraping
* 🔁 Asynchronous support for high throughput
* 🔄 Integrates with Kafka for event publishing

---

## 🧱 Project Structure

```
src/
└── app/
    ├── core/                  # Domain layer
    │   ├── logging/           # Logging setup (optional/custom)
    │   ├── models/            # Core domain models (e.g. Message, ScraperTask)
    │   └── services/          # Reusable logic or integrations (e.g. Kafka producer)
    │
    ├── pipeline/              # Data processing pipeline
    │   ├── stages/            # Individual pipeline steps (e.g. keyword filtering)
    │   ├── base.py            # Pipeline base interface
    │   ├── registry.py        # Dynamic registration of stages
    │   └── pipeline.py        # Main pipeline implementation
    │
    ├── scrapers/              # Data source modules
    │   ├── base.py            # Abstract scraper interface
    │   ├── telegram/          # Telegram scraper implementation
    │   └── nitter/            # Nitter (Twitter frontend) scraper implementation
    │
    ├── main.py                # Application entry point
    └── __init__.py
tests/                         # Unit and integration tests

```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-user/sas.scrapingagent.git
cd sas.scrapingagent
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Edit `config.py` or use `.env` for:

```env
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
SESSION=session_name
DESTINATION=destination_channel_or_user
CHATS=source_channel_ids_or_usernames
KEY_WORDS=keywords,to,filter,by
```

---

## 🧪 Usage

### Run a specific scraper manually

```bash
python -m app.main
```

The main agent will:

* Run enabled scraper tasks
* Fetch, filter, and transform messages
* Optionally send results to a Kafka topic or save locally

---

## ✏️ Adding a New Scraper

1. Create a new folder under `app/scrapers/`
2. Inherit from `BaseScraper`
3. Implement `run_task(self, task: ScraperTask) -> List[Message]`

Example:

```python
class YourCustomScraper(BaseScraper):
    def run_task(self, task: ScraperTask) -> List[Message]:
        ...
```

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 📤 Kafka Integration (optional)

This project can forward results to Kafka topics by implementing a `KafkaProducer` and integrating it into `main.py`.

---

## 📄 License

MIT License
