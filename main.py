import os
import requests
from curl_cffi import requests as cffi_requests

# EVDS API URL (Görünür veri çekmek için tarih aralığı geniş tutulmuştur)
URL = "https://evds3.tcmb.gov.tr/service/evds/series=TP.AB.A02&startDate=01-01-2025&endDate=31-12-2026&type=json&key=El2gYsoqfe"

def verileri_al_ve_gonder():
    try:
        # Chrome 120 parmak izi ile istek atarak Cloudflare/TCMB engelini aşıyoruz
        response = cffi_requests.get(URL, impersonate="chrome120", timeout=30)
        
        if response.status_code != 200:
            print(f"HTTP Hatası: {response.status_code}")
            return

        data = response.json()
        items = data.get("items", [])
        
        # Henüz verisi girilmemiş boş günleri filtreleyelim
        gecerli_veriler = [i for i in items if i.get("TP_AB_A02") is not None]
        
        if gecerli_veriler:
            son_veri = gecerli_veriler[-1]
            tarih = son_veri.get("Tarih", "Bilinmiyor")
            rezerv = son_veri.get("TP_AB_A02", "Bilinmiyor")
            
            mesaj = f"🏛 **TCMB Haftalık Rezerv Verisi**\n\n📅 **Tarih:** {tarih}\n💰 **Toplam Rezerv:** {rezerv} Bin USD"
            print("Gönderilecek Mesaj:\n", mesaj)
            
            # Telegram'a Gönder
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            
            if bot_token and chat_id:
                tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                res = requests.post(tg_url, json={"chat_id": chat_id, "text": mesaj, "parse_mode": "Markdown"})
                print("Telegram Yanıtı:", res.json())
            else:
                print("Telegram Token veya Chat ID eksik!")
        else:
            print("Geçerli rezerv verisi bulunamadı.")
            
    except Exception as e:
        print("Hata oluştu:", e)

if __name__ == "__main__":
    verileri_al_ve_gonder()
