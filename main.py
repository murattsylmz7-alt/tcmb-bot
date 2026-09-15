import os
import requests
from curl_cffi import requests as cffi_requests

# EVDS API URL
URL = "https://evds3.tcmb.gov.tr/service/evds/series=TP.AB.A02&startDate=01-01-2025&endDate=31-12-2026&type=json"

headers = {
    "key": "El2gYsoqfe",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://evds3.tcmb.gov.tr/"
}

def verileri_al_ve_gonder():
    try:
        # API anahtarını URL yerine Header üzerinden göndererek güvenlik kontrolünü aşıyoruz
        response = cffi_requests.get(URL, headers=headers, impersonate="chrome120", timeout=30)
        
        if response.status_code != 200:
            print(f"HTTP Hatası: {response.status_code}")
            print("Gelen Yanıt:", response.text[:200])
            return

        try:
            data = response.json()
        except Exception:
            print("Sunucu JSON döndürmedi. Dönen içerik:")
            print(response.text[:300])
            return

        items = data.get("items", [])
        gecerli_veriler = [i for i in items if i.get("TP_AB_A02") is not None and i.get("TP_AB_A02") != ""]
        
        if gecerli_veriler:
            son_veri = gecerli_veriler[-1]
            tarih = son_veri.get("Tarih", "Bilinmiyor")
            rezerv = son_veri.get("TP_AB_A02", "Bilinmiyor")
            
            mesaj = f"🏛 **TCMB Haftalık Rezerv Verisi**\n\n📅 **Tarih:** {tarih}\n💰 **Toplam Rezerv:** {rezerv} Bin USD"
            print("Gönderilecek Mesaj:\n", mesaj)
            
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            
            if bot_token and chat_id:
                tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                res = requests.post(tg_url, json={"chat_id": chat_id, "text": mesaj, "parse_mode": "Markdown"})
                print("Telegram Yanıtı:", res.json())
            else:
                print("Telegram Secret bilgileri eksik!")
        else:
            print("Geçerli rezerv verisi bulunamadı.")
            
    except Exception as e:
        print("Sistem hatası oluştu:", e)

if __name__ == "__main__":
    verileri_al_ve_gonder()
