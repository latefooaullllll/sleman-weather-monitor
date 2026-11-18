
import requests

from database import save_weather

# Koordinat Kabupaten Sleman
LATITUDE = -7.7167
LONGITUDE = 110.3556

# URL Open-Meteo API
API_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_description(code):
    """Mengubah kode cuaca WMO menjadi deskripsi."""

    weather_codes = {
        0: "Cerah",
        1: "Cerah berawan",
        2: "Berawan sebagian",
        3: "Mendung",
        45: "Berkabut",
        48: "Kabut tebal",
        51: "Gerimis ringan",
        53: "Gerimis sedang",
        55: "Gerimis lebat",
        56: "Gerimis beku ringan",
        57: "Gerimis beku lebat",
        61: "Hujan ringan",
        63: "Hujan sedang",
        65: "Hujan lebat",
        66: "Hujan beku ringan",
        67: "Hujan beku lebat",
        71: "Salju ringan",
        73: "Salju sedang",
        75: "Salju lebat",
        77: "Butiran salju",
        80: "Hujan lokal ringan",
        81: "Hujan lokal sedang",
        82: "Hujan lokal lebat",
        85: "Hujan salju ringan",
        86: "Hujan salju lebat",
        95: "Badai petir",
        96: "Badai petir disertai hujan es ringan",
        99: "Badai petir disertai hujan es lebat"
    }

    return weather_codes.get(code, "Kondisi cuaca tidak diketahui")


def fetch_weather():
    """Mengambil data cuaca dan menyimpannya ke database."""

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m,"
            "weather_code"
        ),
        "timezone": "Asia/Jakarta"
    }

    try:
        print("\nMengambil data cuaca dari Open-Meteo...")

        response = requests.get(
            API_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        result = response.json()
        weather = result["current"]

        condition = get_weather_description(
            weather["weather_code"]
        )

        # Menampilkan data cuaca
        print("\n=== CUACA KABUPATEN SLEMAN ===")
        print(f"Waktu update      : {weather['time']}")
        print(f"Suhu              : {weather['temperature_2m']} °C")
        print(f"Kelembapan        : {weather['relative_humidity_2m']} %")
        print(f"Kecepatan angin   : {weather['wind_speed_10m']} km/jam")
        print(f"Kode cuaca        : {weather['weather_code']}")
        print(f"Kondisi           : {condition}")

        # Menyimpan data ke SQLite
        save_weather(weather, condition)

        return {
            **weather,
            "condition": condition
        }

    except requests.exceptions.RequestException as error:
        print(f"Gagal mengambil data cuaca: {error}")

    except (KeyError, TypeError, ValueError) as error:
        print(f"Data cuaca tidak sesuai format: {error}")

    return None


# Tes jika file dijalankan langsung
if __name__ == "__main__":
    fetch_weather()
