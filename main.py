from dotenv import load_dotenv
import os
import logging
import datetime
import time

from src.bot import Bot
from src.configmanager import ConfigManager
from src.translation.googletranslator import GoogleTranslator

load_dotenv()

log_dir = "/app/data/logs"
os.makedirs(log_dir, exist_ok=True)

# Log retention period in days
log_retention_days = 50

def cleanup_logs(directory, retention_days):
    os.remove("/app/data/logs/latest.log")
    now = time.time()
    retention_seconds = retention_days * 86400 
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and (now - os.path.getmtime(file_path) > retention_seconds):
            os.remove(file_path)
            print(f"Deleted old log file: {file_path}")

cleanup_logs(log_dir, log_retention_days)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Terminal output
        logging.FileHandler("/app/data/logs/latest.log"),
        logging.FileHandler(f"/app/data/logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")  # File output with timestamp
    ]
)

config = ConfigManager(
    valid_translators={
        "google": lambda: GoogleTranslator(logger=logging.getLogger(__name__))
    },
    logger=logging.getLogger(__name__),
)

bot = Bot(
    config_manager=config,
    translator=config.valid_translators[config.get_key("translator")](),
    logger=logging.getLogger(__name__),
)

bot.run(os.getenv('DISCORD_TOKEN'))
