from dotenv import load_dotenv
import os

from src.bot import Bot
from src.configmanager import ConfigManager

from src.translation.googletranslator import GoogleTranslator

load_dotenv()

config = ConfigManager()

bot = Bot(
    config_manager=config,
    translator={
        "google": lambda: GoogleTranslator()
    }.get(config.get_key("translator"), GoogleTranslator)()
)


bot.run(os.getenv('DISCORD_TOKEN'))