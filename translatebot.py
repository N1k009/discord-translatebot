import discord
import os
import sys
from discord.ext import commands
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

# Dil etiketi ceviri
LANG_LABELS = {
    "az": {"user_msg": "İstifadəçi Mesajı", "translation": "Tərcümə"},
    "tr": {"user_msg": "Kullanıcı Mesajı", "translation": "Çeviri"},
    "en": {"user_msg": "User Message", "translation": "Translation"},
    "es": {"user_msg": "Mensaje del Usuario", "translation": "Traducción"},
    "fr": {"user_msg": "Message de l'Utilisateur", "translation": "Traduction"},
    "ru": {"user_msg": "Сообщение пользователя", "translation": "Перевод"},
    "de": {"user_msg": "Benutzernachricht", "translation": "Übersetzung"},
    "zh-CN": {"user_msg": "用户消息", "translation": "翻译"},
    "hi": {"user_msg": "उपयोगकर्ता संदेश", "translation": "अनुवाद"},
    "ar": {"user_msg": "رسالة المستخدم", "translation": "الترجمة"},
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
            await message.add_reaction("🌐")
        except Exception as e:
            print(f"Reaction hatasi: {e}")
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    if str(reaction.emoji) != "🌐":
        return
    
    message = reaction.message
    
    # Kullanici dilini bul
    lang = "en"
    for role in user.roles:
        if role.id in LANG_ROLES:
            lang = LANG_ROLES[role.id]
            break
    
    # Dil etiketlerini al
    labels = LANG_LABELS.get(lang, LANG_LABELS["en"])
    user_msg_label = labels["user_msg"]
    translation_label = labels["translation"]
    
    try:
        # Ceviri yap
        t = GoogleTranslator(source="auto", target=lang).translate(message.content)
        
        # Embed yapısı oluşturma (Mavi renkli ve belirgin başlıklarla)
        embed = discord.Embed(color=discord.Color.blue())
        embed.add_field(name=f"🔵 {user_msg_label}", value=f"{message.author.mention}: {message.content}", inline=False)
        embed.add_field(name=f"📖 {translation_label}", value=f"{t}", inline=False)
        
        # DM gönderme
        await user.send(embed=embed)
        
    except Exception as e:
        print(f"Ceviri hatasi: {e}")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
