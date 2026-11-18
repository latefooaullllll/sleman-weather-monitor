# 🌦️ Sleman Weather Monitor

Sleman Weather Monitor merupakan aplikasi pemantauan cuaca Kabupaten Sleman berbasis Python. Aplikasi ini mengambil informasi cuaca menggunakan Open-Meteo API, menyimpan data ke database SQLite, menampilkan informasi melalui dashboard Streamlit, serta menyediakan notifikasi dan analisis cuaca melalui Telegram Bot yang terintegrasi dengan Gemini AI.

## ✨ Fitur Utama

1. **Weather Scraper**  
   Mengambil data cuaca Kabupaten Sleman dari Open-Meteo API, meliputi suhu, kelembapan, kecepatan angin, dan informasi cuaca lainnya.

2. **Database SQLite**  
   Menyimpan hasil pengambilan data cuaca agar dapat digunakan untuk pemantauan dan analisis.

3. **Telegram Bot**  
   Mengirimkan informasi dan notifikasi cuaca kepada pengguna melalui Telegram.

4. **Streamlit Dashboard**  
   Menampilkan informasi dan visualisasi data cuaca melalui dashboard interaktif.

5. **Gemini AI Integration**  
   Memungkinkan pengguna bertanya dan mendapatkan analisis mengenai kondisi cuaca melalui bantuan Gemini AI.

6. **Automatic Weather Notification**  
   Menjalankan pengiriman informasi cuaca secara otomatis sesuai jadwal yang telah ditentukan.

## 🛠️ Teknologi yang Digunakan

- Python
- Open-Meteo API
- SQLite
- Streamlit
- Telegram Bot API
- Google Gemini API
- Requests
- Python-dotenv

## 📁 Struktur Proyek

```text
sleman_weather_monitor/
│
├── bot.py
├── dashboard.py
├── database.py
├── gemini_ai.py
├── scraper.py
├── requirements.txt
├── .env
├── .gitignore
└── sleman_weather.db
```

## ⚙️ Instalasi dan Konfigurasi

### 1. Clone Repository

```bash
git clone https://github.com/latefooaullllll/sleman-weather-monitor.git
cd sleman-weather-monitor
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

Aktifkan virtual environment di Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment

Buat file `.env` di folder utama proyek dan isi dengan konfigurasi berikut:

```env
TELEGRAM_BOT_TOKEN=isi_token_bot_telegram
GEMINI_API_KEY=isi_api_key_gemini
```

Ganti nilai tersebut dengan token dan API Key milik sendiri. Jangan membagikan file `.env` ke publik.

## ▶️ Menjalankan Aplikasi

### Menjalankan Weather Scraper

```bash
python scraper.py
```

### Menjalankan Telegram Bot

```bash
python bot.py
```

### Menjalankan Dashboard

```bash
streamlit run dashboard.py
```

## 📍 Sumber Data

Data cuaca diperoleh dari [Open-Meteo API](https://open-meteo.com/).

Informasi cuaca diproses menggunakan Python dan disimpan dalam database SQLite untuk mendukung pemantauan serta analisis kondisi cuaca Kabupaten Sleman.

## 🎯 Tujuan Proyek

Proyek ini dibuat sebagai penerapan materi mata kuliah Scripting Language melalui penggunaan Python, API, pengolahan JSON, database, chatbot Telegram, integrasi AI, dan visualisasi data menggunakan Streamlit.

---

**Project:** Sleman Weather Monitor  
**Programming Language:** Python  
**Location:** Kabupaten Sleman, Yogyakarta, Indonesia