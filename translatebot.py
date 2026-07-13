import discord
import os
import sys
from discord.ext import commands
from discord.ui import View, Button
from deep_translator import GoogleTranslator
from keep_alive import keep_alive
from typing import Optional

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

LANG_NAMES = {
    "az": "Azərbaycanca",
    "tr": "Türkçe",
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "ru": "Русский",
    "de": "Deutsch",
    "zh-CN": "中文",
    "hi": "हिन्दी",
    "ar": "العربية",
}

# ==========================
# BOT AYARLARI
# ==========================

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Çeviri önbelleği (cache)
translation_cache = {}

# ==========================
# ÇEVİR BUTONU
# ==========================

class TranslateView(View):
    """Çeviri butonu sistemi"""

    def __init__(self, text: str, message_id: int):
        super().__init__(timeout=None)  # Persistent view
        self.text = text
        self.message_id = message_id

    @discord.ui.button(
        label="🌐 Çevir",
        style=discord.ButtonStyle.primary,
        custom_id="translate_button"
    )
    async def translate_button(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        """Çeviri butonuna tıklandığında çalışır"""

        # Kullanıcının dilini belirle
        target_lang = "en"

        for role in interaction.user.roles:
            if role.id in LANG_ROLES:
                target_lang = LANG_ROLES[role.id]
                break

        # Önbellekte kontrol et
        cache_key = f"{self.message_id}_{target_lang}"

        if cache_key in translation_cache:
            translated = translation_cache[cache_key]
            print(f"✅ Önbellekten çeviri alındı: {cache_key}")
        else:
            try:
                # Çeviyi yap
                translated = GoogleTranslator(
                    source="auto",
                    target=target_lang
                ).translate(self.text)

                # Önbelleğe kaydet
                translation_cache[cache_key] = translated
                print(f"✅ Çeviri yapıldı ve önbelleğe kaydedildi: {cache_key}")

            except Exception as e:
                print(f"❌ Çeviri hatası: {e}")
                await interaction.response.send_message(
                    f"❌ Çeviri hatası:\n`{str(e)}`",
                    ephemeral=True
                )
                return

        # Embed oluştur
        embed = discord.Embed(
            title="🌐 Çeviri",
            description=translated,
            color=discord.Color.blue()
        )

        lang_name = LANG_NAMES.get(target_lang, target_lang)
        embed.set_footer(text=f"Hedef Dil: {lang_name}")

        # Gönder
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

        print(f"✅ Çeviri gönderildi -> {interaction.user}: {lang_name}")

# ==========================
# READY EVENT
# ==========================

@bot.event
async def on_ready():
    """Bot başladığında"""

    print("=" * 40)
    print(f"✅ Giriş Yapıldı: {bot.user}")
    print(f"✅ Sunucu Sayısı: {len(bot.guilds)}")
    print(f"✅ Kullanıcı Sayısı: {len(bot.users)}")
    print("=" * 40)

    # Bot statusu ayarla
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="🌐 Çeviri İçin Butona Bas"
        )
    )

# ==========================
# MESAJ ALGILA
# ==========================

@bot.event
async def on_message(message: discord.Message):
    """Her mesaj alındığında çalışır"""

    # Bot mesajlarını geç
    if message.author.bot:
        return

    # DM mesajlarını geç
    if not message.guild:
        return

    # Boş mesajları geç
    if not message.content.strip():
        return

    # Komutları işle
    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    try:
        # Çeviri butonu ile cevap ver
        view = TranslateView(message.content, message.id)

        await message.reply(
            "🌐 Bu mesajı çevirmek için aşağıdaki butona bas.",
            view=view,
            mention_author=False
        )

        print(f"📨 Mesaj alındı: {message.author} -> {message.content[:50]}")

    except discord.errors.HTTPException as e:
        print(f"❌ HTTP Hatası: {e}")

    except Exception as e:
        print(f"❌ Bilinmeyen Hata: {e}")

    await bot.process_commands(message)

# ==========================
# KOMUTLAR
# ==========================

@bot.command(name="çeviriler", aliases=["languages", "diller"])
async def languages_command(ctx: commands.Context):
    """Desteklenen dilleri göster"""

    embed = discord.Embed(
        title="🌐 Desteklenen Diller",
        color=discord.Color.blue()
    )

    for role_id, lang_code in LANG_ROLES.items():
        lang_name = LANG_NAMES.get(lang_code, lang_code)
        embed.add_field(
            name=f"{lang_name} ({lang_code})",
            value=f"<@&{role_id}>",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command(name="durum")
async def status_command(ctx: commands.Context):
    """Bot durumunu göster"""

    embed = discord.Embed(
        title="📊 Bot Durumu",
        color=discord.Color.green()
    )

    embed.add_field(name="✅ Status", value="Aktif", inline=False)
    embed.add_field(name="📍 Sunucu", value=f"{len(bot.guilds)}", inline=True)
    embed.add_field(name="👥 Kullanıcı", value=f"{len(bot.users)}", inline=True)
    embed.add_field(
        name="💾 Önbellek",
        value=f"{len(translation_cache)} çeviri",
        inline=True
    )

    await ctx.send(embed=embed)

@bot.command(name="yardım")
async def help_command(ctx: commands.Context):
    """Yardım menüsü"""

    embed = discord.Embed(
        title="📖 Yardım",
        description="Çeviri botunun nasıl kullanılacağını öğren",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Nasıl Kullanılır?",
        value="Bir mesaj gönder → 🌐 Çevir butonuna tıkla → Mesaj çevrilir",
        inline=False
    )

    embed.add_field(
        name="Hangi dile çevirir?",
        value="Sahibin olan rol'e göre çeviriri. (Rol yoksa İngilizce)",
        inline=False
    )

    embed.add_field(
        name="Komutlar",
        value="```\n!çeviriler - Dilleri göster\n!durum - Bot durumu\n!yardım - Bu mesaj\n```",
        inline=False
    )

    await ctx.send(embed=embed)

# ==========================
# HATA HANDLER
# ==========================

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    """Komut hatalarını yakala"""

    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Komut Bulunamadı",
            description=f"Komut: `{ctx.message.content}`",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bu komutu kullanmaya izniniz yok.")

    else:
        print(f"❌ Komut Hatası: {error}")
        await ctx.send(f"❌ Bir hata oluştu: `{str(error)}`")

# ==========================
# BAŞLAT
# ==========================

if __name__ == "__main__":
    print("🚀 Bot başlatılıyor...")

    try:
        keep_alive()
        bot.run(TOKEN)

    except Exception as e:
        print(f"❌ Başlatma hatası: {e}")
        sys.exit(1)
