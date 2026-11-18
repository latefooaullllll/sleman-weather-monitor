
import os
import time

from dotenv import load_dotenv
from google import genai

from database import get_latest_weather, get_weather_history

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di file .env.")

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash"
]


def generate_answer(prompt):
    for model in MODELS:
        for percobaan in range(2):
            try:
                print(f"Mencoba model {model}...")

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    print(f"Berhasil menggunakan {model}")

                    jawaban = response.text.strip()
                    jawaban = jawaban.replace("**", "")
                    jawaban = jawaban.replace("*", "")

                    return jawaban

            except Exception as error:
                print(f"Error pada {model}: {error}")

                if "503" in str(error) or "UNAVAILABLE" in str(error):
                    if percobaan == 0:
                        print("Mencoba kembali dalam 3 detik...")
                        time.sleep(3)
                    else:
                        print("Beralih ke model berikutnya.")
                else:
                    return "Terjadi kendala pada Gemini API. Silakan periksa konfigurasi API Key dan akses model."

    return "Maaf, layanan Gemini sedang sibuk. Silakan coba beberapa saat lagi."


def answer_weather_question(question):
    latest = get_latest_weather()
    history = get_weather_history(limit=5)

    if latest is None:
        return "Belum ada data cuaca di database."

    records = {}

    for item in history:
        records[str(item["waktu_update"])] = dict(item)

    records[str(latest["waktu_update"])] = dict(latest)

    data_terurut = sorted(
        records.values(),
        key=lambda item: str(item["waktu_update"])
    )[-5:]

    data_terbaru = (
        f"Waktu: {latest['waktu_update']}\n"
        f"Suhu: {latest['suhu']} °C\n"
        f"Kelembapan: {latest['kelembapan']}%\n"
        f"Kecepatan angin: {latest['kecepatan_angin']} km/jam\n"
        f"Kondisi: {latest['kondisi']}"
    )

    data_riwayat = ""

    for nomor, item in enumerate(data_terurut, start=1):
        data_riwayat += (
            f"\nData {nomor}:\n"
            f"Waktu: {item['waktu_update']}\n"
            f"Suhu: {item['suhu']} °C\n"
            f"Kelembapan: {item['kelembapan']}%\n"
            f"Kecepatan angin: {item['kecepatan_angin']} km/jam\n"
            f"Kondisi: {item['kondisi']}\n"
        )

    prompt = f"""
Kamu adalah asisten analisis cuaca untuk Sleman Weather Monitor.

Gunakan bahasa Indonesia yang natural, sederhana, ramah,
dan mudah dipahami.

DATA CUACA TERBARU:
{data_terbaru}

RIWAYAT CUACA:
Data diurutkan dari waktu paling lama ke waktu paling baru.
{data_riwayat}

KEMAMPUAN ANALISIS:
1. Menjelaskan kondisi cuaca terbaru.
2. Membandingkan suhu, kelembapan, dan kecepatan angin
   dengan data sebelumnya.
3. Menghitung besar kenaikan atau penurunan jika datanya tersedia.
4. Menjelaskan kecenderungan perubahan cuaca dari riwayat.
5. Memberikan saran aktivitas berdasarkan kondisi cuaca aktual.

ATURAN:
1. Gunakan hanya data yang tersedia.
2. Jangan mengarang angka, kondisi, atau prakiraan cuaca.
3. Jangan menyimpulkan kemungkinan hujan hanya dari kondisi mendung.
4. Jika data sebelumnya tidak tersedia, jelaskan keterbatasannya.
5. Bedakan antara perubahan angka dan penyebab perubahan.
6. Jangan mengarang penyebab perubahan suhu, kelembapan,
   atau kecepatan angin.
7. Gunakan satuan °C, persen, dan km/jam.
8. Jawaban harus ringkas tetapi informatif.
9. Jangan gunakan format Markdown atau tanda bintang.
10. Gunakan tanda strip jika memang perlu membuat daftar.
11. Jangan mengulang seluruh data jika tidak diperlukan.

PERTANYAAN PENGGUNA:
{question}
"""

    return generate_answer(prompt)


if __name__ == "__main__":
    print("=== TES GEMINI AI ===")

    pertanyaan = input("Masukkan pertanyaan tentang cuaca: ")

    if pertanyaan.strip():
        jawaban = answer_weather_question(pertanyaan)
        print("\nJawaban Gemini:")
        print(jawaban)
    else:
        print("Pertanyaan tidak boleh kosong.")
