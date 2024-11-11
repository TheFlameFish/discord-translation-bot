# Lesson learned: Do unit testing stuff first

import logging
import os
from unittest.mock import AsyncMock, MagicMock, Mock
import pytest
import discord
from discord.ext import commands
from src.bot import Bot
from src.logic.config_logic import ConfigLogic
from src.translation.translator import Translator
from src.configmanager import ConfigManager

import json

@pytest.fixture
def mock_ctx(mock_member) -> AsyncMock:
    ctx = AsyncMock()
    ctx.send = AsyncMock()
    ctx.respond = AsyncMock()
    ctx.author = mock_member
    return ctx

def mock_logger() -> MagicMock:
    logger = MagicMock(spec=logging.Logger)
    logger.getChild = lambda name: mock_logger()
    logger.info = lambda *args: print(f"INFO: {' '.join(map(str, args))}")
    logger.warn = lambda *args: print(f"WARNING: {' '.join(map(str, args))}")
    return logger

mock_config_dict = {
        "permissions": {
            "use_translation": {
                "Multilingual": True
            },
            "config.read": {
                "@everyone": True
            },
            "config.general_write": {
                "@everyone": True
            },
            "config.manage_perms": {
                "@everyone": True
            }
        },
        "reaction_translations": True,
        "translator": "google"
    }

@pytest.fixture
def mock_config_manager() -> MagicMock:
    config = MagicMock()
    config.get_key = lambda key: mock_config_dict[key]
    config.get.return_value = mock_config_dict
    config.has_permission.return_value = True

    return config

@pytest.fixture
def mock_member() -> MagicMock:
    member = MagicMock(spec=discord.Member)
    member.name = "TestUser"

    everyone = MagicMock(spec=discord.Role)
    everyone.name = "@everyone"

    member.roles = [
        everyone
    ]
    return member

@pytest.fixture
def actual_config_manager() -> ConfigManager:
    config = ConfigManager(
        logger=mock_logger(),
        config_path="test/data/config.json"
    )

    # Future me problem =)
    # 5 minutes later: Future me is now present me! Nooooo!
    # config.has_permission = lambda user, permission: True 

    print(type(config))

    yield config

    cleanup()

def test_list_command(mock_ctx, actual_config_manager):
    for i in range(2): # Run twice, once with config files not existing, once with them existing
        print(type(actual_config_manager))
        config = ConfigLogic(
                    config=actual_config_manager,
                    logger=mock_logger()
                )

        print(mock_ctx.author.name)
        print(mock_ctx.author.roles)

        output_list = config.list_config(mock_ctx.author)

        assert output_list != "You do not have the required permission."

        start = output_list.find("{")
        end = output_list.rfind("}") + 1
        output_list = output_list[start:end]

        assert json.loads(
                output_list
            ) == config.config.config # Lovely
    
def test_has_permissions(mock_member, actual_config_manager):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    config.config.config["permissions"]["use_translation"] = {}

    assert config._check_permission(mock_member, "config.read") == None
    assert config._check_permission(mock_member, "config.manage_perms") == None
    assert config._check_permission(mock_member, "config.general_write") == None
    assert config._check_permission(mock_member, "config.nonexistent") == "You do not have the required permission."
    assert config._check_permission(mock_member, "config.use_translation") == "You do not have the required permission."

def test_add_permission_command(mock_ctx, actual_config_manager):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    output = config.add_permission(mock_ctx.author, "Multilingual", "use_translation")

    assert output == "Added permission 'use_translation' to role 'Multilingual'."

    assert config.config.config["permissions"]["use_translation"]["Multilingual"] == True

def test_remove_permission_command(mock_ctx, actual_config_manager):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    output = config.remove_permission(mock_ctx.author, "@everyone", "use_translation")

    assert output == "Removed permission 'use_translation' from role '@everyone'."

    # Should be None or False (With current behavior it'll be none I think)
    assert not config.config.config["permissions"]["use_translation"].get("@everyone")

def test_set_reaction_translations_command(mock_ctx, actual_config_manager):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    output = config.set_reaction_translations(mock_ctx.author, False)

    assert output == "Set reaction translations to 'False'."

    assert not config.config.config["reaction_translations"]

    output = config.set_reaction_translations(mock_ctx.author, True)

    assert output == "Set reaction translations to 'True'."

    assert config.config.config["reaction_translations"]

def test_set_translator_command(mock_ctx, actual_config_manager):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    output = config.set_translator(mock_ctx.author, "google")

    assert output == "Set translator to 'google'."

    assert config.config.config["translator"] == "google"

    output = config.set_translator(mock_ctx.author, "⁉️")
    print(output.splitlines()[0])
    assert output.splitlines()[0] == "Invalid translator '⁉️'."

def test_get_permissions_for_user_command(mock_ctx, actual_config_manager, mock_member):
    config = ConfigLogic(
                config=actual_config_manager,
                logger=mock_logger()
            )

    output = config.get_permissions_for_user(mock_ctx.author, mock_member)

    assert output != "You do not have the required permission."

    assert output != None # I'm not sure how to best test this.

# Not really a test...
def cleanup():
    if os.path.exists("test/data/config.json"):
        os.remove("test/data/config.json")
        os.rmdir("test/data")