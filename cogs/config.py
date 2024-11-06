import discord
from discord.ext import commands

import config
import localization

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Config cog loaded")
        config.load()

    config_group = discord.SlashCommandGroup(name="config", description="Configuration commands")

    def config_list_embed(self, dictionary: dict):
        embed = discord.Embed(title="Configuration")

        def add_subfields(d, title=""):
            for key, value in d.items():
                if isinstance(value, dict):
                    nested_text = ""
                    for sub_key, sub_value in value.items():
                        nested_text += f"`{sub_key}`: `{sub_value}`\n"
                    embed.add_field(name=f"{title}{key}", value=nested_text, inline=False)
                else:
                    # If it's not a dictionary, add it directly
                    embed.add_field(name=f"{title}{key}", value=f"`{value}`", inline=False)

        add_subfields(dictionary)  # Add all top-level items and subfields

        return embed


    @config_group.command(name_localizations=localization.get_locale_dict("command.config.list.name"),
                          guild_ids=[1020794656189067305])
    async def list(self, ctx: discord.ApplicationContext):
        if config.has_permission(ctx.author, "config.read"):
            print("User ", ctx.author.display_name, " requested config list.")
            await ctx.respond(embed=self.config_list_embed(config.get()))
        else:
            print("Config: Read permission denied for user ", ctx.author.display_name)
            await ctx.send_response(localization.get("permission.error.config.read_denied", ctx.interaction.locale),
                                    ephemeral=True)


def setup(bot):
    bot.add_cog(Config(bot))
