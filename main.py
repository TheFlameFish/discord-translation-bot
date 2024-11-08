from dotenv import load_dotenv
import os
import logging
import logging.config

from src.bot import Bot
from src.configmanager import ConfigManager

from src.translation.googletranslator import GoogleTranslator
import datetime

load_dotenv()

log_dir = "/app/data/logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Terminal output
        logging.FileHandler("/app/data/logs/latest.log"),
        logging.FileHandler(f"/app/data/logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log") # File output with timestamp
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