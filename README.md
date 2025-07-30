# 🕷️ SAS.ScrapingAgent

**SAS.ScrapingAgent** is a scalable, modular scraping service that collects and processes real-time data from platforms like **Telegram**, **Nitter**, **Twitter (API)**, and others. It is part of a larger microservices-based system designed for monitoring and detecting local events such as crimes and disasters using social media content.

---

## 📦 Features

* 🔌 Supports multiple scraping sources (Telegram, Nitter, Twitter, etc.)
* 📄 Extracts structured data
* 🎯 Pipeline for preprocessing and filtering
* ⚙️ Easily extendable with new scraper modules
* 🛠 Uses **Selenium**, **Playwright**, or **API** for scraping
* 🔁 Asynchronous support for high throughput
* 🔄 Integrates with Kafka for event publishing

---

## 🧱 Project Structure

```
src/
└── app/
    ├── core/                  # Domain layer
    ├── pipeline/              # Data processing pipeline
    ├── scrapers/              # Scraper modules (Telegram, Twitter, etc.)
    │   └── sources/
    │       ├── telegram/
    │       ├── twitter/       # ✅ NEW: Twitter API scraper
    │       ├── nitter/
    │       └── dummy/
    ├── kafka/                 # Kafka consumer/producer integrations
    └── main.py                # Entry point
tests/                         # Unit & performance tests
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hasankhadd0ur/sas.scrapingagent.git
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

---

## 🧪 Usage

### Run scrapers manually

```bash
python -m app.main
```

The main agent will:

* Load active scraping tasks
* Run platform-specific scrapers (Telegram, Twitter, etc.)
* Filter and transform collected messages
* Optionally publish them to Kafka or store locally

---

## ✏️ Adding a New Scraper

1. Create a module under `app/scrapers/sources/`
2. Inherit from `BaseScraper`
3. Implement:

```python
async def run_task(self, task: ScrapingTask) -> AsyncGenerator[List[Message], None]
```

Example:

```python
class MyScraper(BaseScraper):
    async def run_task(self, task):
        # your scraping logic
        yield [Message(...), ...]
```

Then register your scraper in `scrapers_registry.py`.

---

## 📤 Kafka Integration (optional)

The system can forward messages to Kafka. See:

* `kafka_producer.py`
* `messages_publishing_stage.py`

To enable:

1. Add Kafka configuration to your config service.
2. Include `MessagesPublishingStage` in your pipeline.

---

## 🧪 Running Tests

```bash
pytest tests/
```

---

## 🧩 Supported Scrapers

| Source       | Method   | File                                                      |
| ------------ | -------- | --------------------------------------------------------- |
| Telegram     | API/Web  | `telegram_telethon_scraper.py`, `telegram_web_scraper.py` |
| Twitter      | API (v2) | `twitter_api_scraper.py`                                  |
| Nitter       | Web      | `nitter_web_scraper.py`                                   |
| Dummy Source | File     | `dummy_file_scrarper.py`                                  |

---

## 📄 License

MIT License

