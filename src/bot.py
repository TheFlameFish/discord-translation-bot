import discord
import src.configmanager as configmanager
from src.translation.translator import Translator
from typing import Type

class Bot(discord.Bot):
    def __init__(self, config_manager: configmanager.ConfigManager, translator: Type[Translator]):
        intents = discord.Intents.all()
        super().__init__(intents=intents,
                         description="Translation bot")
        
        self.config = config_manager
        self.translator = translator

        # Add cogs
        self.load_extension("src.cogs.translation")
        self.load_extension("src.cogs.config")

    async def on_ready(self):
        print(f"{self.user} is ready and online.")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name="you")
        )

