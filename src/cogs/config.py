import discord
from discord.ext import commands
from src.logic.config_logic import ConfigLogic
import src.localization as localization
from src.bot import Bot

class Config(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = bot.parent_logger.getChild(__name__)
        localization.load(log=self.logger)
        self.config_logic = ConfigLogic(bot.config, self.logger)

    config_group = discord.SlashCommandGroup(
        name="config",
        name_localizations=localization.get_locale_dict("command.config.name")
    )

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.list.name"),
        guild_ids=[1020794656189067305]
    )
    async def list(self, ctx: discord.ApplicationContext):
        await ctx.respond(self.config_logic.list_config(ctx.author))

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.check_permissions.name")
    )
    async def list_permissions(self, ctx: discord.ApplicationContext, user: discord.Member):
        await ctx.respond(self.config_logic.get_permissions_for_user(ctx.author, user))

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.add_permission.name")
    )
    async def add_permission(self, ctx: discord.ApplicationContext, role: discord.Role, permission: str):
        await ctx.respond(self.config_logic.add_permission(ctx.author, role.name, permission))

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.remove_permission.name")
    )
    async def remove_permission(self, ctx: discord.ApplicationContext, role: discord.Role, permission: str):
        await ctx.respond(self.config_logic.remove_permission(ctx.author, role.name, permission))

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.set_reaction_translations.name")
    )
    async def set_reaction_translations(self, ctx: discord.ApplicationContext, value: bool):
        await ctx.respond(self.config_logic.set_reaction_translations(ctx.author, value))

    @config_group.command(
        name_localizations=localization.get_locale_dict("command.config.set_translator.name")
    )
    async def set_translator(self, ctx: discord.ApplicationContext, translator: str):
        await ctx.respond(self.config_logic.set_translator(ctx.author, translator))

def setup(bot: Bot):
    bot.add_cog(Config(bot))
