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

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

if not TOKEN:
    print("❌ DISCORD_BOT_TOKEN bulunamadı!")
    sys.exit(1)

# ==========================
# DİL ROLLERİ
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
# BOT
# ==========================

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ==========================
# ÇEVİR BUTONU
# ==========================

class TranslateView(View):

    def __init__(self, text):
        super().__init__(timeout=300)
        self.text = text

    @discord.ui.button(
        label="🌐 Çevir",
        style=discord.ButtonStyle.primary
    )
    async def translate_button(self, interaction: discord.Interaction, button: Button):

        target_lang = "en"

        for role in interaction.user.roles:
            if role.id in LANG_ROLES:
                target_lang = LANG_ROLES[role.id]
                break

        try:

            translated = GoogleTranslator(
                source="auto",
                target=target_lang
            ).translate(self.text)

            embed = discord.Embed(
                title="🌐 Çeviri",
                description=translated,
                color=discord.Color.blue()
            )

            embed.set_footer(
                text=f"Hedef Dil: {target_lang}"
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )

        except Exception as e:

            await interaction.response.send_message(
                f"❌ Çeviri hatası:\n{e}",
                ephemeral=True
            )

# ==========================
# READY
# ==========================

@bot.event
async def on_ready():

    print("=================================")
    print(f"✅ Giriş Yapıldı : {bot.user}")
    print(f"✅ Sunucu Sayısı : {len(bot.guilds)}")
    print("=================================")

# ==========================
# MESAJ ALGILAMA
# ==========================

@bot.event
async def on_message(message):

    print(f"Mesaj: {message.author} -> {message.content}")

    # Bot mesajlarını geç
    if message.author.bot:
        return

    # Boş mesajları geç
    if not message.content:
        return

    # Komutları geç
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    try:

        await message.reply(
            "🌐 Bu mesajı çevirmek için aşağıdaki butona bas.",
            view=TranslateView(message.content),
            mention_author=False
        )

    except Exception as e:

        print("Mesaj gönderilemedi:", e)

    await bot.process_commands(message)

# ==========================
# BAŞLAT
# ==========================

if __name__ == "__main__":

    keep_alive()

    bot.run(TOKEN)
