import asyncio
import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pytest

from app.core.models.scraper_task import DataSource
from app.scrapers.sources.telegram.telegram_web_scraper import TelegramWebScraper
from app.core.configs.env_config import EnvConfig

# === Mocked Task and Scraper Setup ===

class MockScrapingTask:
    def __init__(self, id="mock-task"):
        self.id = id
        self.domain = "Test"
        self.platform = "telegram"
        self.sources = [
            DataSource(target="freesyria102", limit=124),
            DataSource(target="Almohrar", limit=124),
            DataSource(target="MQ_QU", limit=130)
        ]
        self.limit = 100
        self.scraping_approach = None


class MockScraper:
    def __init__(self, delay=0.1, batch_size=10):
        self.delay = delay
        self.batch_size = batch_size

    async def run_task(self, task):
        while True:
            await asyncio.sleep(self.delay)
            yield [{"id": i} for i in range(self.batch_size)]


# === 1-Minute Benchmark Test ===

@pytest.mark.asyncio
@pytest.mark.parametrize("duration_minutes", [10])
async def test_mock_scraper_benchmark(duration_minutes):
    scraper =TelegramWebScraper(EnvConfig())
    task = MockScrapingTask()
    
    end_time = datetime.datetime.now() + datetime.timedelta(minutes=duration_minutes)
    stats = defaultdict(int)
    total_scraped = 0

    print(f"\n📊 Starting {duration_minutes}-minute benchmark at {datetime.datetime.now().strftime('%H:%M:%S')}", flush=True)

    async for batch in scraper.run_task(task):
        now = datetime.datetime.now()
        if now > end_time:
            break
        time_key = now.replace(microsecond=0)
        stats[time_key] += len(batch)
        total_scraped += len(batch)
        print(f"[{time_key.strftime('%H:%M:%S')}] Scraped {len(batch)} messages. Total: {total_scraped}", flush=True)

    # === Save to CSV ===
    csv_path = "scraper_benchmark_results.csv"
    with open(csv_path, "w") as f:
        f.write("timestamp,messages_scraped\n")
        for t in sorted(stats.keys()):
            f.write(f"{t.strftime('%H:%M:%S')},{stats[t]}\n")
    print(f"📄 Results saved to {csv_path}", flush=True)

    # === Plotting ===
    timestamps = sorted(stats.keys())
    counts = [stats[t] for t in timestamps]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(timestamps, counts, marker='.', linestyle='-', color='steelblue', linewidth=2)
    ax.set_title(f"Mock Scraper Benchmark - {duration_minutes} Minute")
    ax.set_xlabel("Time")
    ax.set_ylabel("Messages Scraped")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # === Stats Summary ===
    mean = np.mean(counts)
    std = np.std(counts)
    max_count = np.max(counts)
    min_count = np.min(counts)
    plt.figtext(0.99, 0.01,
                f"Total: {total_scraped} | Mean: {mean:.2f} | Std: {std:.2f} | Max: {max_count} | Min: {min_count}",
                ha='right', fontsize=9, bbox={"facecolor": "lightgrey", "alpha": 0.5, "pad": 4})

    img_path = "scraper_benchmark_plot.png"
    plt.savefig(img_path)
    plt.show()
    print(f"📊 Plot saved to {img_path}", flush=True)

    print(f"\n✅ Total messages scraped in {duration_minutes} minutes: {total_scraped}", flush=True)
    assert total_scraped > 0, "Mock scraper did not retrieve any messages."
