import discord
import os
import sys
from discord.ext import commands
from discord.ui import View, Button
from deep_translator import GoogleTranslator
from langdetect import detect
from keep_alive import keep_alive

# ==========================
# TOKEN
# ==========================

TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

if not TOKEN:
    print("HATA: DISCORD_BOT_TOKEN bulunamadi!")
    sys.exit(1)

# ==========================
# DIL ROLLERI
# ==========================

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

# Dil kodları karşılaştırması
LANG_MAP = {
    "az": "az",
    "tr": "tr",
    "en": "en",
    "es": "es",
    "fr": "fr",
    "ru": "ru",
    "de": "de",
    "zh-CN": "zh-cn",
    "zh": "zh-cn",
    "hi": "hi",
    "ar": "ar",
}

# ==========================
# BOT AYARLARI
# ==========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# CEVIRI BUTONU
# ==========================

class TranslateView(View):
    def __init__(self, text, user_lang):
        super().__init__(timeout=300)
        self.text = text
        self.user_lang = user_lang

    @discord.ui.button(label="", emoji="🌐", style=discord.ButtonStyle.gray)
    async def translate_button(self, interaction: discord.Interaction, button: Button):
        """Ceviri butonuna tiklandiginda calisir"""
        
        try:
            # Textin dilini tespit et
            detected_lang = detect(self.text)
            detected_lang = LANG_MAP.get(detected_lang, detected_lang)
            
            # Eger zaten kullanici dilindeyse cevir etme
            if detected_lang == self.user_lang:
                await interaction.response.send_message(
                    f"Bu mesaj zaten {self.user_lang} dilinde!",
                    ephemeral=True
                )
                return
            
            # Ceviri yap
            translated = GoogleTranslator(
                source="auto",
                target=self.user_lang
            ).translate(self.text)
            
            # Sonucu goster
            await interaction.response.send_message(
                f"**Orijinal:** {self.text}\n\n**Ceviri:** {translated}",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"Ceviri hatasi: {str(e)}",
                ephemeral=True
            )

# ==========================
# BOT OLAYLARI
# ==========================

@bot.event
async def on_ready():
    print(f"Bot baslatildi: {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="mesajlari ceviriyor"
        )
    )

@bot.event
async def on_message(message):
    # Bot mesajlarini gec
    if message.author.bot:
        return
    
    # DM'leri gec
    if not message.guild:
        return
    
    # Bos mesajlari gec
    if not message.content.strip():
        return
    
    # Kullanicinin dilini bul
    user_lang = "en"
    for role in message.author.roles:
        if role.id in LANG_ROLES:
            user_lang = LANG_ROLES[role.id]
            break
    
    # Komut degilse ceviri butonunu ekle
    if not message.content.startswith("!"):
        try:
            # Mesajin dilini tespit et
            detected_lang = detect(message.content)
            detected_lang = LANG_MAP.get(detected_lang, detected_lang)
            
            # Eger zaten kendi dilindeyse buton gosterme
            if detected_lang != user_lang:
                view = TranslateView(message.content, user_lang)
                await message.add_reaction("🌐")
                
        except Exception as e:
            print(f"Hata: {e}")
    
    # Komutlari isle
    await bot.process_commands(message)

# ==========================
# BASLA
# ==========================

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
