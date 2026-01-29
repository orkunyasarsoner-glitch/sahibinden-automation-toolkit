from DrissionPage import ChromiumPage, ChromiumOptions
import time
import random
import pyautogui

# ==========================================
# 1. BİLGİLERİNİ BURAYA YAZ
# ==========================================
# Not: Lütfen şifreni kodun içinde saklarken dikkatli ol!
GERCEK_KULLANICI_ADI = "GERCEK_KULLANICI_ADI"
GERCEK_SIFRE = "Şifre" 

TARGET_URL = "https://secure.sahibinden.com/giris"
# Güvenlik
pyautogui.FAILSAFE = True 

def hibrit_islem(page, selector, metin=None):
    try:
        eleman = page.ele(selector)
        if eleman:
            # --- MOUSE HAREKETİ (GÖRSEL ŞOV) ---
            rect = eleman.run_js('return this.getBoundingClientRect().toJSON()')
            
            # URL barına tıklamaması için ofseti koruyoruz
            toolbar_offset = 180 
            
            final_x = rect['x'] + (rect['width'] / 2)
            final_y = rect['y'] + toolbar_offset + (rect['height'] / 2)
            
            print(f"👀 Mouse {selector} hedefine gidiyor...")
            pyautogui.moveTo(final_x, final_y, duration=random.uniform(0.6, 1.1))
            
            # --- TIKLAMA VE ODAKLANMA ---
            pyautogui.click()       # Fiziksel tıklama (görüntü için)
            eleman.run_js("this.focus()") # Yazılımsal odaklanma (garanti için)
            
            # --- YAZMA İŞLEMİ (KRİTİK DÜZELTME) ---
            if metin:
                time.sleep(0.5)
                # pyautogui YERİNE DrissionPage kullanıyoruz.
                # Bu yöntem klavye dilinden etkilenmez, @ işaretini kesin yazar.
                for harf in metin:
                    # clear=False demezsek her harfte kutuyu temizler
                    eleman.input(harf, clear=False) 
                    time.sleep(random.uniform(0.05, 0.15)) # İnsan hızı efekti
            
            time.sleep(0.5)
            return True
        else:
            print(f"❌ Bulunamadı: {selector}")
            return False
    except Exception as e:
        print(f"⚠️ Hata: {e}")
        return False

def baslat():
    print("🚀 FİNAL BOT BAŞLATILIYOR (@ SORUNU GİDERİLDİ)...")
    print("⚠️ Mouse hareket edecek. Lütfen dokunma.")
    
    co = ChromiumOptions()
    co.set_argument('--no-first-run')
    co.set_argument('--start-maximized') 
    
    page = ChromiumPage(co)
    
    try:
        page.get(TARGET_URL)
        print("🌍 Sayfa açıldı, bekleniyor...")
        time.sleep(4)
        
        # 1. KULLANICI ADI
        print("👤 Kullanıcı adı giriliyor...")
        hibrit_islem(page, '#username', GERCEK_KULLANICI_ADI)
        
        # 2. ŞİFRE
        print("🔑 Şifre giriliyor...")
        hibrit_islem(page, '#password', GERCEK_SIFRE)
        
        # 3. GİRİŞ BUTONU
        print("👆 Giriş butonuna tıklanıyor...")
        if not hibrit_islem(page, '#userLoginSubmitButton'):
            hibrit_islem(page, 'text=Giriş Yap')

        print("\n✨ İşlem tamamlandı. Klavye sorunu çözüldü.")
        
    except Exception as e:
        print(f"Genel Hata: {e}")

if __name__ == "__main__":
    baslat()