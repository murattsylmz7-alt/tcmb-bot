import os
import requests

# EVDS API URL
URL = "https://evds3.tcmb.gov.tr/service/evds/series=TP.AB.A02&startDate=01-01-2026&endDate=31-12-2026&type=json&key=El2gYsoqfe"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def verileri_al_ve_gonder():
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        data = response.json()
        
        items = data.get("items", [])
        if items:
            son_veri = items[-1]
            tarih = son_veri.get("Tarih", "Bilinmiyor")
            rezerv = son_veri.get("TP_AB_A02", "Bilinmiyor")
            
            mesaj = f"🏛 **TCMB Haftalık Rezerv Verisi**\n\n📅 **Tarih:** {tarih}\n💰 **Toplam Rezerv:** {rezerv} Bin USD"
            print(mesaj)
            
            # Telegram'a Gönder
            bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            chat_id = os.environ.get("TELEGRAM_CHAT_ID")
            
            if bot_token and chat_id:
                tg_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                requests.post(tg_url, json={"chat_id": chat_id, "text": mesaj, "parse_mode": "Markdown"})
        else:
            print("Veri bulunamadı.")
    except Exception as e:
        print("Hata oluştu:", e)

if __name__ == "__main__":
    verileri_al_ve_gonder()
