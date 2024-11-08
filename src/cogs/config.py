import json
import discord
from discord.ext import commands

from src.bot import Bot
import src.localization as localization

from src.translation.googletranslator import GoogleTranslator

class Config(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        self.config = bot.config
        self.logger = bot.parent_logger.getChild(__name__)

        localization.load(log=self.logger)

    config_group = discord.SlashCommandGroup(
        name="config",
        name_localizations = localization.get_locale_dict("command.config.name")
    )

    @config_group.command(
            name_localizations = localization.get_locale_dict("command.config.list.name"),
            guild_ids=[1020794656189067305]
    )
    async def list(self, ctx: discord.ApplicationContext):
        if not self.config.has_permission(ctx.author, "config.read"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to read the config.")
            await ctx.send_response(localization.get("permission.error.config.read_denied", ctx.interaction.locale), 
                                    ephemeral=True)
        self.logger.info("List command triggered.")

        await ctx.respond(f"# Config: \n{
            json.dumps(self.config.get(), indent=4)}")
        
    @config_group.command(
        name_localizations = localization.get_locale_dict("command.config.check_permissions.name")
    )
    async def list_permissions(self, ctx: discord.ApplicationContext, user: discord.Member):
        if not self.config.has_permission(ctx.author, "config.read"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to read permissions.")
            await ctx.send_response(localization.get("permission.error.config.read_denied", ctx.interaction.locale), 
                                    ephemeral=True)
        self.logger.info("Check permissions command triggered.")

        await ctx.respond(f"# Permissions for user '{user.name}': \n{
            json.dumps(self.config.get_permissions(user), indent=4)}")
        
    @config_group.command(
        name_localizations = localization.get_locale_dict("command.config.add_permission.name")
    )
    async def add_permission(self, ctx: discord.ApplicationContext, role: discord.Role, permission: str):
        if not self.config.has_permission(ctx.author, "config.manage_perms"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to manage permissions.")
            await ctx.send_response(localization.get("permission.error.config.manage_perms_denied", ctx.interaction.locale), 
                                    ephemeral=True)
            return

        self.logger.info("Add permission command triggered.")

        try:
            self.config.add_permission(role.name, permission)
        except KeyError:
            await ctx.send_response(f"Permission '{permission}' does not exist.", ephemeral=True)
            return
        await ctx.respond(f"Added permission '{permission}' to role '{role.name}'.")

    @config_group.command(
        name_localizations = localization.get_locale_dict("command.config.remove_permission.name")
    )
    async def remove_permission(self, ctx: discord.ApplicationContext, role: discord.Role, permission: str):
        if not self.config.has_permission(ctx.author, "config.manage_perms"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to manage permissions.")
            await ctx.send_response(localization.get("permission.error.config.manage_perms_denied", ctx.interaction.locale), 
                                    ephemeral=True)
            return

        self.logger.info("Remove permission command triggered.")

        try:
            self.config.remove_permission(role.name, permission)
        except KeyError:
            await ctx.send_response(f"Permission '{permission}' does not exist.", ephemeral=True)
            return
        await ctx.respond(f"Removed permission '{permission}' from role '{role.name}'.")

    @config_group.command(
        name_localizations = localization.get_locale_dict("command.config.set_reaction_translations.name")
    )
    async def set_reaction_translations(self, ctx: discord.ApplicationContext, value: bool):
        if not self.config.has_permission(ctx.author, "config.general_write"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to adjust config.")
            await ctx.send_response(localization.get("permission.error.config.write_denied", ctx.interaction.locale), 
                                    ephemeral=True)
            return

        self.logger.info("Set reaction translations command triggered.")

        self.config.set("reaction_translations", value)
        await ctx.respond(f"Set reaction translations to '{value}'.")

    @config_group.command(
        name_localizations = localization.get_locale_dict("command.config.set_translator.name")
    )
    async def set_translator(self, ctx: discord.ApplicationContext, translator: str):
        if not self.config.has_permission(ctx.author, "config.general_write"):
            self.logger.info(f"User '{ctx.author.name}' does not have permission to adjust config.")
            await ctx.send_response(localization.get("permission.error.config.write_denied", ctx.interaction.locale), 
                                    ephemeral=True)
            return

        self.logger.info("Set translator command triggered.")

        if translator not in self.config.valid_translators:
            await ctx.send_response(f"Invalid translator '{translator}'.\nValid translators are: {self.config.valid_translators}", ephemeral=True)
            return

        self.config.set("translator", translator)
        self.bot.translator = self.config.valid_translators[translator]()
        await ctx.respond(f"Set translator to '{translator}'.")

def setup(bot: Bot):
    bot.add_cog(Config(bot))