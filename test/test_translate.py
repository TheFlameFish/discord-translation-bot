# Test the translation command and reaction translations

import logging
from unittest.mock import AsyncMock, MagicMock, Mock
import pytest
import discord
from discord.ext import commands
from src.bot import Bot
from src.cogs.translation import Translation

# Translators
import src.translation.googletranslator as googletranslator

translators = [
    lambda: googletranslator.GoogleTranslator(MagicMock())
]

@pytest.fixture
def mock_ctx() -> AsyncMock:
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.respond = AsyncMock()
    ctx.author = MagicMock()
    return ctx

def mock_logger():
    logger = MagicMock(spec=logging.Logger)  # Ensure it's a mock of a Logger instance
    logger.getChild = lambda name: mock_logger()
    logger.info = lambda x: print(f"INFO: {x}")
    return logger

def mock_config_manager():
    config = MagicMock()
    config.get_key.return_value = True
    config.has_permission.return_value = True

    return config

@pytest.fixture
def mock_message(content = "Hello") -> MagicMock:
    message = MagicMock()
    message.content = content
    message.author = MagicMock()
    message.reply = AsyncMock()

    return message

def add_fetches(bot: Bot, mock_message):
    bot.fetch_user = AsyncMock()
    bot.fetch_user.return_value.name = "TestUser"
    bot.get_guild = MagicMock()
    bot.get_guild.return_value.fetch_member = AsyncMock(return_value="TestMember")
    bot.get_channel = MagicMock()
    bot.get_channel.return_value.fetch_message = AsyncMock(return_value=mock_message)

@pytest.mark.parametrize("translator", translators)
@pytest.mark.asyncio
async def test_translate_command(translator, mock_ctx):
    bot = Bot(
        config_manager=mock_config_manager(),
        translator = translator(),
        logger=mock_logger()
    )

    translator: Translation = Translation(bot)

    print(bot.commands)

    await translator.translate(mock_ctx, "Hello", "es")

    mock_ctx.respond.assert_awaited_once()

    print("\n\nArgs: {mock_ctx.respond.call_args}")
    
    

@pytest.mark.parametrize("translator", translators)
@pytest.mark.asyncio
async def test_on_raw_reaction_add(translator, mock_message):
    bot = Bot(
        config_manager=mock_config_manager(),
        translator = translator(),
        logger=mock_logger()
    )

    translator: Translation = Translation(bot)

    # Mock payload and bot channel/message fetching
    mock_payload = MagicMock()
    mock_payload.user_id = 123456789
    mock_payload.guild_id = 987654321
    mock_payload.channel_id = 555555555
    mock_payload.message_id = 999999999
    mock_payload.emoji = discord.PartialEmoji(name="🇪🇸")

    # Fetch methods
    add_fetches(bot, mock_message)

    # Call on_raw_reaction_add manually
    await translator.on_raw_reaction_add(mock_payload)
    # await bot.on_raw_reaction_add(mock_payload)

    # Assertions
    bot.get_channel.assert_called_with(mock_payload.channel_id)  # Check channel fetching
    bot.get_channel.return_value.fetch_message.assert_called_with(mock_payload.message_id)  # Check message fetching
    mock_message.reply.assert_called_once()  # Ensure reply was called
