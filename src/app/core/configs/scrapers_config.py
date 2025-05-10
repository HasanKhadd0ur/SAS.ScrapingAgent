BASE_CONFIG = {
    "batch_size": 5
}

DUMMY_SCRAPER_CONFIG = {
    **BASE_CONFIG,
    "file_path": "../assets/mini-sample.jsonl",
    "delay": 0.05,
}


TELEGRAM_WEB_SCRAPER_CONFIG = {
    **BASE_CONFIG,
    "delay": 0.2, 
    "selector": "div.tgme_widget_message_text"
}

