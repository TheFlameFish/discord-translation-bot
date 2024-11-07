from dotenv import load_dotenv
import os

from src.bot import Bot
from src.configmanager import ConfigManager

from src.translation.googletranslator import GoogleTranslator

load_dotenv()

config = ConfigManager(
    valid_translators={
        "google": lambda: GoogleTranslator()
    }
)

bot = Bot(
    config_manager=config,
    translator=config.valid_translators[config.get_key("translator")]()
)

bot.run(os.getenv('DISCORD_TOKEN'))