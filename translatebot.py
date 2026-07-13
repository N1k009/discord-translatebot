import discord
import os
import sys
from discord.ext import commands
from deep_translator import GoogleTranslator
from keep_alive import keep_alive

# Token okuma
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')
if not TOKEN:
    sys.exit(1)

# ID'ler burada, asla kaybolmayacaklar
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
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Hazır: {bot.user}")

@bot.event
async def on_message(message):
    # Kendi kendine tetiklenmeyi engelle
    if message.author.id == bot.user.id:
        return
    
    # Sadece normal mesajlara emoji ekle
    if message.content and not message.content.startswith("!"):
        await message.add_reaction("🌐")
    
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    # Botun kendi eklediği emojiyi veya başkasının emojisini değil, sadece 🌐'yi yakala
    if payload.user_id == bot.user.id or str(payload.emoji) != "🌐":
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)
    user = await guild.fetch_member(payload.user_id)

    # Dil seçimi
    lang = "en"
    for r in user.roles:
        if r.id in LANG_ROLES:
            lang = LANG_ROLES[r.id]
            break
            
    try:
        translated = GoogleTranslator(source="auto", target=lang).translate(message.content)
        await user.send(f"**🌐 Çeviri:**\n{translated}")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
