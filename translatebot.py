import discord
import os
import sys
from discord.ext import commands
from discord.ui import View, Button
from deep_translator import GoogleTranslator
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
    def __init__(self, text, target_lang):
        super().__init__(timeout=300)
        self.text = text
        self.target_lang = target_lang

    @discord.ui.button(label="", emoji="🌐", style=discord.ButtonStyle.gray)
    async def translate_button(self, interaction: discord.Interaction, button: Button):
        """Ceviri butonuna tiklandiginda calisir"""
        
        try:
            # Ceviri yap
            translated = GoogleTranslator(
                source="auto",
                target=self.target_lang
            ).translate(self.text)
            
            # Sonucu goster (ephemeral - sadece kullanici gorur)
            await interaction.response.send_message(
                f"**Orijinal:** {self.text}\n\n**Ceviri ({self.target_lang}):** {translated}",
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
    
    # Komut degilse ceviri butonunu ekle
    if not message.content.startswith("!"):
        try:
            # Kullanicinin dilini bul
            user_lang = "en"
            for role in message.author.roles:
                if role.id in LANG_ROLES:
                    user_lang = LANG_ROLES[role.id]
                    break
            
            # Ceviri butonunu ekle
            view = TranslateView(message.content, user_lang)
            await message.reply(
                "",
                view=view,
                mention_author=False
            )
            
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
