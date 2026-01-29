import pyautogui
import time
import subprocess
import os
import pyperclip  # Kopyala-Yapıştır için (pip install pyperclip)

# ==========================================
# 🛠️ AYARLAR
# ==========================================
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
SITE_URL = "https://secure.sahibinden.com/giris"

MAIL_ADRESIN = "GERCEK_KULLANICI_ADI"
SIFREN = "Şifre"
# ==========================================

def baslat():
    print("💉 JS ENJEKSİYON BOTU BAŞLATILIYOR...")
    
    # 1. Temiz Chrome'u aç
    print("🌍 Sayfa açılıyor...")
    if os.path.exists(CHROME_PATH):
        subprocess.Popen([CHROME_PATH, SITE_URL, "--new-window"])
    else:
        print("⚠️ Chrome bulunamadı! Elle aç.")
    
    # Sayfanın yüklenmesini bekle
    print("⏳ Sayfa yükleniyor (5 sn)...")
    time.sleep(5)
    
    print("⚡ Kod enjekte ediliyor...")

    # 2. Adres Çubuğuna Odaklan (CTRL + L)
    # Bu kısayol her tarayıcıda adres çubuğunu seçer.
    pyautogui.hotkey('ctrl', 'l') 
    time.sleep(0.5)
    
    # 3. JavaScript Kodunu Hazırla
    # Chrome güvenliği yüzünden 'javascript:' kelimesini yapıştırınca siler.
    # O yüzden önce 'javascript:' kelimesini elle yazdıracağız, gerisini yapıştıracağız.
    
    js_kodu = f"document.getElementById('username').value='{MAIL_ADRESIN}';" \
              f"document.getElementById('password').value='{SIFREN}';" \
              f"document.getElementById('userLoginSubmitButton').click();"

    # 'javascript:' kısmını yaz
    pyautogui.write("javascript:", interval=0.05)
    
    # Geri kalan uzun kodu panoya kopyala ve yapıştır (Hız için)
    pyperclip.copy(js_kodu)
    pyautogui.hotkey('ctrl', 'v')
    
    time.sleep(0.5)
    
    # 4. Çalıştır
    pyautogui.press('enter')
    
    print("🎉 KOMUT GÖNDERİLDİ! Giriş yapılmış olmalı.")

if __name__ == "__main__":
    # pyperclip kütüphanesi yoksa uyaralım
    try:
        import pyperclip
        baslat()
    except ImportError:
        print("Lütfen önce şu komutu çalıştır: pip install pyperclip")