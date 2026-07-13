import discord
import os
import sys
from discord.ext import commands
from discord.ui import View, Button
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("HATA: DISCORD_BOT_TOKEN bulunamadı!")
    sys.exit(1)

LANG_ROLES = {
    1526232723",
    1526233568043602062: "fr",
    1526275300738990133: "ru",
    1526275400194592778: "de",
    1526233733752033411: "zh-CN",
    1526233677053562890: "hi",
    1526233633650901132: "en",
    1526233508610310256: "es",
    1526233568043602062: "fr",
    1526275300738990133: "ru",
    1526275400194592778: "de",
    1526233733752033411: "zh-CN",
    1526233677053562029758073: "az",
    1526233376678481920: "tr",
    1526233442616868974: "en",
    1526233508610310256: "es",
    1526233568043602062: "fr",
    1526275300738990133: "ru: "ar",
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class TV(View):
    def __init__(self, text):
        super().__init__(timeout=300)
        self.text = text

    @discord.ui.button(label="🌐 Çevir", style=discord.ButtonStyle.primary)
    async def tr(self, interaction: discord.Interaction, button: Button):
        lang = "en"
        for r in interaction890: "hi",
    1526233633650901132: "ar",
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class TV(View):
    def __init__(self, text):
        super().__init__(timeout=300)
        self.text = text

    @discord.ui.button(label="🌐 Çevir", style=discord.ButtonStyle.primary)
    async def tr(self, interaction: discord.Interaction",
    1526275400194592778: "de",
    1526233733752033411: "zh-CN",
    1526233677053562890: "hi",
    1526233633650901132: "ar",
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=", button: Button):
        lang = "en"
        for r in interaction.user.roles:
            if r.id in LANG_ROLES:
                lang = LANG_ROLES[r.id]
                break
        try:
            t = GoogleTranslator(source="auto", target=lang).translate(self.text)
            await interaction.response.send_message(
                embed=discord.Embed(title="🌐 Çeviri.user.roles:
            if r.id in LANG_ROLES:
                lang = LANG_ROLES[r.id]
                break
        try:
            t = GoogleTranslator(source="auto", target=lang).translate(self.text)
            await interaction.response.send_message(
                embed=discord.Embed(title="🌐 Çeviri", description=t),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(f"Hata: {str", description=t),
                ephemeral=True
            )
        except Exception as e:
            await interaction.response(e)}", ephemeral=True)

@.send_message(f"Hata: {str(e)}", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ Bot Hazır: {bot.user}")

@bot.event
async def on_message(message):
    print(f"📨 Mesaj: {message.author} -> {message.content[:50]}")
    
    if message.author.bot:
        return
    
    if not message.guild:
        return
    
    if message.content and not message.content.startswith("!"):
        try:
            await message.reply(
                "Bu mesajı çevirmek için butona bas.",
                view=TVbot.event
async def on_ready():
    print(f"✅ Bot Hazır: {bot.user}")

@bot.event
async def on_message(message):
    # Bot mesajlarını geç
    if message.author.bot:
        return
    
    # DM'leri geç
    if not message.guild:
        return
    
    # Komut değilse çeviri butonu gönder
    if message.content and not message.content.startswith("!"):
        try:
            await message.reply(!", intents=intents)

class TV(View):
    def __init__(self, text):
        super().__init__(timeout=300)
        self.text = text

    @discord.ui.button(label="🌐 Çevir", style=discord.ButtonStyle.primary)
    async def tr(self, interaction: discord.Interaction, button: Button):
        lang = "en"
        for r in interaction.user.roles:
            if r.id in LANG_ROLES:
                lang = LANG_ROLES[r.id]
                break
        try:
            t = GoogleTranslator(source="auto", target=lang).(message.content),
                mention_author=False
            )
            print("✅ Çeviri mesajı gönderildi")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    # BU SATIR EN SONDA OLMALI!
    await bot.process_commands(message)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
