import logging
from unittest.mock import AsyncMock, MagicMock, Mock
import pytest
import discord
from discord.ext import commands
from src.bot import Bot
from src.cogs.config import Config
from src.translation.translator import Translator

@pytest.fixture
def mock_ctx() -> AsyncMock:
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.respond = AsyncMock()
    ctx.author = MagicMock()
    return ctx

def mock_logger() -> MagicMock:
    logger = MagicMock(spec=logging.Logger)
    logger.getChild = lambda name: mock_logger()
    logger.info = lambda x: print(f"INFO: {x}")
    logger.warn = lambda x: print(f"WARNING: {x}")
    return logger

def mock_config_manager() -> MagicMock:
    config = MagicMock()
    config.get_key.return_value = True
    config.has_permission.return_value = True

    return config

@pytest.mark.asyncio
async def test_list_command(mock_ctx):
    config = Config(
                Bot(
                    config_manager=mock_config_manager(), 
                    logger=mock_logger(),
                    translator=Translator()
                )
            )
    
    

    await config.list(mock_ctx)
    mock_ctx.respond.assert_awaited_once()