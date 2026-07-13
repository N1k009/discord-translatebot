import discord
import os
import sys
from discord.ext import commands
from discord.ui import View, Button
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("HATA: DISCORD_BOT_TOKEN bulunamadi!")
    sys.exit(1)

LANG_ROLES = {
    1526232723029758073: "az",
    1526233376678481920: "tr",
    1526233442616868974: "en",
    1526233508610310256: "es",
    1526233568043602062: "fr",
    1526275300738990133: "ru",
    1526275400194592778: "de",
    1526233733752033411: "zh-CN",
    1526233677053562890: "hi",
    1526233633650901132: "ar",
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

class TranslateView(View):
    def __init__(self, text):
        super().__init__(timeout=300)
        self.text = text

    @discord.ui.button(label="", emoji="🌐", style=discord.ButtonStyle.gray)
    async def translate_button(self, interaction: discord.Interaction, button: Button):
        lang = "en"
        for role in interaction.user.roles:
            if role.id in LANG_ROLES:
                lang = LANG_ROLES[role.id]
                break
        
        try:
            t = GoogleTranslator(source="auto", target=lang).translate(self.text)
            embed = discord.Embed(title="Ceviri", description=t)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Hata: {str(e)}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot Hazir: {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not message.guild:
        return
    
    if message.content and not message.content.startswith("!"):
        try:
            view = TranslateView(message.content)
            await message.reply(
                "‏",  # Zero-width space (görünmez)
                view=view,
                mention_author=False
            )
        except Exception as e:
            print(f"Hata: {e}")
    
    await bot.process_commands(message)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
