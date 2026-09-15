import os
import requests

# CSV formatı Cloudflare/EVDS JSON filtresine takılmaz
URL = "https://evds3.tcmb.gov.tr/service/evds/series=TP.AB.A02&startDate=01-01-2025&endDate=31-12-2026&type=csv&key=El2gYsoqfe"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def verileri_al_ve_gonder():
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        
        # Yanıt metnini al
        metin = response.text.strip()
        
        # Eğer HTML döndüyse uyar
        if "<!DOCTYPE" in metin or "<html" in metin:
            print("TCMB sunucusu HTML engel sayfası döndürdü.")
            return

        satirlar = [s for s in metin.splitlines() if s.strip()]
        
        if len(satirlar) > 1:
            # En son açıklanan rezerv satırını al
            son_satir = satirlar[-1]
            
            # CSV ayırıcı kontrolü (virgül veya noktalı virgül)
            ayrac = ";" if ";" in son_satir else ","
            parcalar = son_satir.split(ayrac)
            
            tarih = parcalar[0].replace('"', '')
            rezerv = parcalar[1].replace('"', '') if len(parcalar) > 1 else "Bilinmiyor"
            
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
            print("Veri satırı bulunamadı.")
            
    except Exception as e:
        print("Hata oluştu:", e)

if __name__ == "__main__":
    verileri_al_ve_gonder()
