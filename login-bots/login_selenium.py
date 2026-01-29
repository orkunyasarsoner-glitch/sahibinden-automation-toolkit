import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import random
import os

# ==========================================
# 🛠️ AYARLAR
# ==========================================
SAHIBINDEN_MAIL = "GERCEK_KULLANICI_ADI"
SAHIBINDEN_SIFRE = "Şifre"

def basili_tut_gec(driver):
    """
    Cloudflare 'Basılı Tutunuz' butonuna fiziksel basılı tutma yapar.
    """
    print("🛡️ Doğrulama ekranı tespit edildi, çözüm deneniyor...")
    time.sleep(2)
    
    try:
        # Iframe içinde mi diye kontrol et
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                if "cloudflare" in iframe.get_attribute("src") or "turnstile" in iframe.get_attribute("src"):
                    driver.switch_to.frame(iframe)
                    print("   ➡️ Cloudflare çerçevesine (iframe) girildi.")
                    break
            except:
                pass

        # Butonu bul (Genelde checkbox veya wrapper olur)
        buton = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox'], .ctp-checkbox-label, #challenge-stage, .big-button"))
        )
        
        print("   ⚔️ Buton bulundu! Basılı tutuluyor...")
        
        action = ActionChains(driver)
        action.move_to_element(buton)
        action.click_and_hold()
        # 5-6 Saniye basılı tut (İnsan gibi)
        action.pause(random.uniform(5, 6))
        action.release()
        action.perform()
        
        print("   ✅ Mouse bırakıldı.")
        driver.switch_to.default_content() # Ana sayfaya dön
        time.sleep(4)
        return True

    except Exception as e:
        print(f"   ⚠️ Basılı tutma hatası: {e}")
        driver.switch_to.default_content()
        return False

def sahibinden_giris():
    print("🟡 Sahibinden Botu Başlatılıyor...")
    
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-popup-blocking')
    
    # Profil kaydet ki her seferinde doğrulama sormasın
    base_path = os.getcwd()
    profile_path = os.path.join(base_path, "Sahibinden_User_Data")
    options.add_argument(f"--user-data-dir={profile_path}")

    driver = uc.Chrome(options=options, use_subprocess=True)
    
    try:
        # Önce Anasayfaya git (Direkt giriş linkine gidince bazen hata veriyor)
        driver.get("https://www.sahibinden.com")
        print("🌍 Siteye gidildi...")
        time.sleep(4)

        # --- ADIM 1: ANASAYFADA MIYIZ? ---
        if "Giriş Yap" in driver.page_source:
            print("🏠 Anasayfadayız. 'Giriş Yap' butonu aranıyor...")
            try:
                # Giriş yap butonunu bul ve tıkla
                giris_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "secure-login-link"))
                )
                giris_btn.click()
                print("👆 'Giriş Yap'a tıklandı.")
            except:
                # ID ile bulamazsa Text ile bul
                try:
                    driver.find_element(By.LINK_TEXT, "Giriş Yap").click()
                    print("👆 'Giriş Yap'a (Metin) tıklandı.")
                except:
                    # O da olmazsa zorla linke git
                    print("⚠️ Buton bulunamadı, linke zorla gidiliyor...")
                    driver.get("https://secure.sahibinden.com/giris")
        
        time.sleep(3)

        # --- ADIM 2: DOĞRULAMA EKRANI GELDİ Mİ? ---
        if "Olağan dışı" in driver.title or "hloading" in driver.current_url:
             print("🚨 DİKKAT: Doğrulama ekranı geldi!")
             # 3 kere dene
             for i in range(3):
                 if "Olağan dışı" in driver.title or "hloading" in driver.current_url:
                     basili_tut_gec(driver)
                 else:
                     break

        # --- ADIM 3: GİRİŞ BİLGİLERİ ---
        print("✍️ Giriş ekranı kontrol ediliyor...")
        
        # Kullanıcı Adı
        try:
            kadi = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "username")))
            # Önce temizle
            kadi.send_keys(Keys.CONTROL + "a")
            kadi.send_keys(Keys.BACKSPACE)
            time.sleep(0.5)
            # Harf harf yaz
            for harf in SAHIBINDEN_MAIL:
                kadi.send_keys(harf)
                time.sleep(0.1)
            print("   ✅ Mail yazıldı.")
        except:
            print("⚠️ Mail kutusu bulunamadı (Zaten giriş yapılmış olabilir).")

        time.sleep(1)
        
        # Şifre
        try:
            sifre = driver.find_element(By.ID, "password")
            sifre.send_keys(SAHIBINDEN_SIFRE)
            print("   ✅ Şifre yazıldı.")
            
            # Giriş Butonu
            btn = driver.find_element(By.ID, "userLoginSubmitButton")
            # JS ile tıkla (daha sağlam)
            driver.execute_script("arguments[0].click();", btn)
            print("👆 Giriş butonuna basıldı.")
        except:
            pass
        
        print("🏁 İşlem tamam. Sonucu izle...")
        time.sleep(120)

    except Exception as e:
        print(f"HATA: {e}")
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    sahibinden_giris()