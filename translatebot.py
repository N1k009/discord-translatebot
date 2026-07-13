import discord
import os
import sys
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

# Token ve Rol Listesi aynı kalıyor
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
LANG_ROLES = {
    1526232723029758073: "az", 1526233376678481920: "tr",
    1526233442616868974: "en", 1526233508610310256: "es",
    1526233568043602062: "fr", 1526275300738990133: "ru",
    1526275400194592778: "de", 1526233733752033411: "zh-CN",
    1526233677053562890: "hi", 1526233633650901132: "ar",
}

# Botu başlat (komutlar için özel bir setup)
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    # Bu satır, sağ tık menüsüne "Çevir" komutunu otomatik ekler
    await bot.tree.sync() 
    print(f"Bot Hazır: {bot.user}")

# Mesajın sağına eklenen sağ tık komutu
@bot.tree.context_menu(name="Mesajı Çevir")
async def translate_message(interaction: discord.Interaction, message: discord.Message):
    # Dil seçimi
    lang = "en"
    for r in interaction.user.roles:
        if r.id in LANG_ROLES:
            lang = LANG_ROLES[r.id]
            break
            
    try:
        translated = GoogleTranslator(source="auto", target=lang).translate(message.content)
        # Sadece basan kişiye özel, kanalda görünür mesaj
        await interaction.response.send_message(f"**🌐 Çeviri:**\n{translated}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Hata: {e}", ephemeral=True)

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
