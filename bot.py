
import os
import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scraper import fetch_weather
from database import (
    get_latest_weather,
    get_weather_history,
    save_chat_id,
    get_chat_ids
)
from gemini_ai import answer_weather_question

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")


def daftar_perintah():
    return (
        "Gunakan perintah berikut:\n"
        "/cuaca - Melihat cuaca terbaru\n"
        "/cekcuaca - Mengambil data terbaru dari API\n"
        "/riwayat - Melihat 5 data cuaca terakhir\n"
        "/tanya - Bertanya tentang cuaca menggunakan AI\n"
        "/analisis - Analisis perubahan cuaca otomatis\n"
        "/tesotomatis - Menguji pengiriman cuaca otomatis\n"
        "/bantuan - Melihat daftar perintah"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_chat_id(chat_id)

    pesan = (
        "Halo! Selamat datang di Sleman Weather Monitor 🌤️\n\n"
        "Kamu berhasil terdaftar untuk menerima informasi "
        "cuaca otomatis setiap hari pukul 07.00 WIB.\n\n"
        + daftar_perintah()
    )

    await update.message.reply_text(pesan)


async def bantuan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pesan = (
        "📋 DAFTAR PERINTAH BOT\n\n"
        + daftar_perintah()
        + "\n\nNotifikasi cuaca harian dikirim otomatis "
        "setiap pukul 07.00 WIB."
    )

    await update.message.reply_text(pesan)


async def cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_latest_weather()

    if data is None:
        await update.message.reply_text(
            "Belum ada data cuaca. Gunakan /cekcuaca terlebih dahulu."
        )
        return

    pesan = (
        "🌤️ CUACA KABUPATEN SLEMAN\n\n"
        f"🕒 Waktu data cuaca: {data['waktu_update']}\n"
        f"🌡️ Suhu: {data['suhu']} °C\n"
        f"💧 Kelembapan: {data['kelembapan']}%\n"
        f"💨 Kecepatan angin: {data['kecepatan_angin']} km/jam\n"
        f"☁️ Kondisi: {data['kondisi']}"
    )

    await update.message.reply_text(pesan)


async def cek_cuaca(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sedang mengambil data cuaca...")

    data = await asyncio.to_thread(fetch_weather)

    if data is None:
        await update.message.reply_text(
            "Maaf, data cuaca gagal diambil. Silakan coba lagi."
        )
        return

    waktu_cek = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%Y-%m-%d %H:%M:%S WIB")

    pesan = (
        "🌤️ DATA CUACA TERBARU\n\n"
        f"🕒 Waktu data cuaca: {data['time']}\n"
        f"🔄 Waktu pengecekan: {waktu_cek}\n"
        f"🌡️ Suhu: {data['temperature_2m']} °C\n"
        f"💧 Kelembapan: {data['relative_humidity_2m']}%\n"
        f"💨 Kecepatan angin: {data['wind_speed_10m']} km/jam\n"
        f"☁️ Kondisi: {data['condition']}"
    )

    await update.message.reply_text(pesan)


async def riwayat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_weather_history(limit=5)

    if not data:
        await update.message.reply_text(
            "Belum ada riwayat data cuaca."
        )
        return

    pesan = "📊 5 RIWAYAT CUACA TERAKHIR\n\n"

    for nomor, item in enumerate(data, start=1):
        pesan += (
            f"{nomor}. {item['waktu_update']}\n"
            f"   Suhu: {item['suhu']} °C\n"
            f"   Kondisi: {item['kondisi']}\n\n"
        )

    await update.message.reply_text(pesan)


async def tanya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertanyaan = " ".join(context.args).strip()

    if not pertanyaan:
        await update.message.reply_text(
            "Silakan masukkan pertanyaan setelah perintah /tanya.\n\n"
            "Contoh:\n"
            "/tanya Bagaimana kondisi cuaca Sleman sekarang?"
        )
        return

    pesan_proses = await update.message.reply_text(
        "🤖 Gemini AI sedang menganalisis data cuaca...\n"
        "Mohon tunggu sebentar."
    )

    try:
        jawaban = await asyncio.to_thread(
            answer_weather_question,
            pertanyaan
        )

        await pesan_proses.edit_text(
            f"🤖 JAWABAN GEMINI AI\n\n{jawaban}"
        )

    except Exception as error:
        print(f"Kesalahan Gemini AI: {error}")

        await pesan_proses.edit_text(
            "Maaf, terjadi kendala saat memproses pertanyaan. "
            "Silakan coba kembali beberapa saat lagi."
        )


async def analisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pertanyaan = (
        "Buat analisis cuaca Kabupaten Sleman berdasarkan data terbaru "
        "dan lima data riwayat terakhir. Jelaskan kondisi cuaca saat ini, "
        "perubahan suhu, kelembapan, dan kecepatan angin dibandingkan "
        "pengukuran sebelumnya. Hitung besar kenaikan atau penurunan "
        "jika datanya tersedia. Berikan kesimpulan singkat dan saran "
        "aktivitas berdasarkan kondisi aktual. Jangan membuat prakiraan "
        "cuaca atau mengarang penyebab perubahan."
    )

    pesan_proses = await update.message.reply_text(
        "📊 Gemini AI sedang menganalisis riwayat cuaca Sleman...\n"
        "Mohon tunggu sebentar."
    )

    try:
        jawaban = await asyncio.to_thread(
            answer_weather_question,
            pertanyaan
        )

        await pesan_proses.edit_text(
            f"📊 ANALISIS CUACA KABUPATEN SLEMAN\n\n{jawaban}"
        )

    except Exception as error:
        print(f"Kesalahan analisis cuaca: {error}")

        await pesan_proses.edit_text(
            "Maaf, analisis cuaca gagal dilakukan. "
            "Silakan coba kembali beberapa saat lagi."
        )


async def kirim_cuaca_otomatis(bot):
    print("\nMenjalankan pengambilan cuaca otomatis...")

    data = await asyncio.to_thread(fetch_weather)

    if data is None:
        print("Pengambilan data cuaca gagal.")
        return

    waktu_cek = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%Y-%m-%d %H:%M:%S WIB")

    pesan = (
        "🌤️ INFORMASI CUACA HARIAN\n\n"
        "📍 Kabupaten Sleman\n\n"
        f"🕒 Waktu data cuaca: {data['time']}\n"
        f"🔄 Waktu pengiriman: {waktu_cek}\n"
        f"🌡️ Suhu: {data['temperature_2m']} °C\n"
        f"💧 Kelembapan: {data['relative_humidity_2m']}%\n"
        f"💨 Kecepatan angin: {data['wind_speed_10m']} km/jam\n"
        f"☁️ Kondisi: {data['condition']}"
    )

    chat_ids = get_chat_ids()

    if not chat_ids:
        print("Belum ada pengguna terdaftar.")
        return

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=pesan)
            print(f"Cuaca berhasil dikirim ke {chat_id}")
        except Exception as error:
            print(f"Gagal mengirim ke {chat_id}: {error}")


async def tes_otomatis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sedang menguji pengiriman cuaca otomatis..."
    )

    await kirim_cuaca_otomatis(context.bot)


async def post_init(application):
    scheduler.add_job(
        kirim_cuaca_otomatis,
        trigger="cron",
        hour=7,
        minute=0,
        args=[application.bot],
        id="daily_weather",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler berhasil diaktifkan!")
    print("Pengiriman cuaca otomatis: setiap hari pukul 07.00 WIB")


async def post_shutdown(application):
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler berhasil dihentikan.")


def main():
    if not TOKEN:
        raise ValueError("Token Telegram belum ditemukan. Periksa file .env.")

    app = (
        Application.builder()
        .token(TOKEN)
        .post_init(post_init)
        .post_shutdown(post_shutdown)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bantuan", bantuan))
    app.add_handler(CommandHandler("cuaca", cuaca))
    app.add_handler(CommandHandler("cekcuaca", cek_cuaca))
    app.add_handler(CommandHandler("riwayat", riwayat))
    app.add_handler(CommandHandler("tanya", tanya))
    app.add_handler(CommandHandler("analisis", analisis))
    app.add_handler(CommandHandler("tesotomatis", tes_otomatis))

    print("Sleman Weather Monitor Bot sedang berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
