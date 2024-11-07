import discord
from discord.ext import commands

from src.bot import Bot
import src.localization as localization

class Translation(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

        self.translator = bot.translator
        self.config = bot.config

    @discord.command(
                name_localizations = localization.get_locale_dict("command.translate.name"),
                description_localizations = localization.get_locale_dict("command.translate.description"))
    async def translate_command(self, ctx: discord.ApplicationContext, text, target_language):
        print("Translate command triggered.")

        if not self.config.has_permission(ctx.author,"use_translation"): # Permission denied
            print(f"User '{ctx.author.name}' does not have permission to use translations.")
            await ctx.send_response(localization.get("command.translate.error.permission", ctx.interaction.locale), ephemeral=True)
            return

        if not target_language:
            await ctx.respond(localization.get("command.translate.error.no_target", ctx.interaction.locale))
            return
        elif not text:
            await ctx.respond(localization.get("command.translate.error.no_text", ctx.interaction.locale))
            return

        translation = self.translator.translate(text=text, target_language=target_language)

        if not translation:
            await ctx.respond(localization.get("command.translate.error.invalid_target",
                                                ctx.interaction.locale, 
                                                language=target_language))
            return

        await ctx.respond(embed=await self.translate_embed(content = translation, 
                                                    author = ctx.author))
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not self.config.get_key("reaction_translations"):
            return

        # Fetch the user who added the reaction
        user = await self.bot.fetch_user(payload.user_id)
        member = await self.bot.get_guild(payload.guild_id).fetch_member(user.id)

        if not self.config.has_permission(member,"use_translation"): # Permission denied
            print(f"User '{user.name}' does not have permission to use translations.")
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        print(f"Reaction added by '{user.name}' with emoji '{payload.emoji.name}' to message '{message.content}'")

        lang = self.translator.get_from_emoji(payload.emoji.name)

        if lang:
            print(f"Detected language: {lang}.")
            translation = self.translator.translate(message.content, lang)

            if not translation:
                print("Failed to translate. Attempting to translate embed.")
                embed, content = self.embed_translation(embed= message.embeds[0], language= lang, user_requested= user,
                                                is_from_me= (message.author == self.bot.user))
                await message.reply(mention_author= False, embed= embed, content= content)
                return
            
            await message.reply(mention_author= False, 
                                embed = await self.translate_embed(content= translation,
                                                            requester= user,
                                                            author= message.author))
        else:
            print("No language detected.")
            return

    def embed_translation(self, embed: discord.Embed, language: str, user_requested: discord.user, is_from_me: bool = False):
        '''Translates an embed.
        Not to be confused with translate_embed(), which generates an embed for translation messages.'''

        new_embed = discord.Embed(
            title = self.translator.translate(embed.title, language) if embed.title else None,
            description = self.translator.translate(embed.description, language) if embed.description else None,
            color = embed.color
        )

        if embed.author:
            new_embed.set_author(
                name = embed.author.name,
                icon_url = embed.author.icon_url
            )

        for field in embed.fields:
            new_embed.add_field(
                name = self.translator.translate(field.name, language),
                value = self.translator.translate(field.value, language),
                inline = field.inline
            )

        content = f"Requested by {user_requested.display_name}"
        if not embed.footer or is_from_me:
            new_embed.set_footer(text = f"Requested by {user_requested.display_name}", icon_url= user_requested.avatar.url)
            content = None
        else:
            new_embed.set_footer(text = self.translator.translate(embed.footer.text, language), icon_url= embed.footer.icon_url)

        return new_embed, content


    async def translate_embed(self, content, author, requester = None):
        '''Generates an embed for translation messages.'''

        print("Creating embed")
        # Creating the embed
        embed = discord.Embed(
            description=content,  # Main description
            color=discord.Color.blue()  # Set the color (customizable)
        )
        
        if requester:
            embed.set_footer(text=f"Requested by {requester.display_name}", icon_url=requester.avatar.url)
        if author:
            embed.set_author(name=author.display_name, icon_url= author.avatar.url if author.avatar else author.default_avatar)

        return embed


def setup(bot):
    bot.add_cog(Translation(bot))


    