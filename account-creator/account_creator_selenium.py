from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import undetected_chromedriver as uc

class CloudflareBypassBot:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.actions = None
        self.tarayici_baslat()
    
    def tarayici_baslat(self):
        """Undetected ChromeDriver ile bot tespitini tamamen engelle"""
        print("🚀 Gelişmiş tarayıcı başlatılıyor...")
        
        try:
            options = uc.ChromeOptions()
            
            # Gerçek kullanıcı gibi ayarlar
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--lang=tr-TR')
            
            # User-Agent
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
            options.add_argument(f'user-agent={user_agent}')
            
            # ÖNEMLİ: version_main parametresini KALDIRDIK
            # undetected-chromedriver otomatik olarak doğru versiyonu bulacak
            self.driver = uc.Chrome(options=options, use_subprocess=True)
            
            # Ekstra bot tespiti engelleyiciler
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Wait ve Actions
            self.wait = WebDriverWait(self.driver, 20)
            self.actions = ActionChains(self.driver)
            
            print("✅ Gelişmiş tarayıcı hazır!")
            
        except Exception as e:
            print(f"❌ Tarayıcı başlatma hatası: {e}")
            print("\n🔧 Alternatif yöntem deneniyor...")
            
            # Alternatif: Normal Selenium (basit ama çalışır)
            self.driver = uc.Chrome()
            self.wait = WebDriverWait(self.driver, 20)
            self.actions = ActionChains(self.driver)
            print("✅ Tarayıcı başlatıldı (alternatif yöntem)")
    
    def cloudflare_bekle(self, max_bekleme=30):
        """Cloudflare kontrolünü bekle ve geç"""
        print("\n🛡️  Cloudflare kontrolü bekleniyor...")
        
        baslangic = time.time()
        
        while time.time() - baslangic < max_bekleme:
            try:
                # "Tarayıcınızı kontrol ediyoruz" yazısını kontrol et
                if "Tarayıcınızı kontrol ediyoruz" in self.driver.page_source:
                    print("⏳ Cloudflare kontrolü devam ediyor...")
                    time.sleep(2)
                    continue
                
                # "Please try again" kontrolü
                if "Please try again" in self.driver.page_source:
                    print("⚠️  Cloudflare hala engel oluyor...")
                    time.sleep(3)
                    continue
                
                # Eğer kayıt sayfası yüklendiyse başarılı
                if "E-posta adresi" in self.driver.page_source or "Hesap aç" in self.driver.page_source:
                    print("✅ Cloudflare kontrolü geçildi!")
                    return True
                
                time.sleep(1)
                
            except Exception as e:
                print(f"⚠️  Kontrol hatası: {e}")
                time.sleep(1)
        
        print("❌ Cloudflare kontrolü geçilemedi!")
        return False
    
    def insan_gibi_yaz(self, element, metin):
        """İnsan gibi yazma"""
        try:
            self.actions.move_to_element(element).pause(random.uniform(0.3, 0.7)).click().perform()
            time.sleep(random.uniform(0.2, 0.5))
            
            element.clear()
            time.sleep(random.uniform(0.1, 0.3))
            
            for i, harf in enumerate(metin):
                element.send_keys(harf)
                
                if harf == ' ':
                    time.sleep(random.uniform(0.15, 0.3))
                elif harf in ['@', '.', '_']:
                    time.sleep(random.uniform(0.12, 0.25))
                elif i > 0 and i % random.randint(4, 6) == 0:
                    time.sleep(random.uniform(0.15, 0.4))
                else:
                    time.sleep(random.uniform(0.08, 0.18))
                
                if random.random() < 0.02:
                    yanlis_harf = random.choice('abcdefghijk')
                    element.send_keys(yanlis_harf)
                    time.sleep(random.uniform(0.1, 0.2))
                    element.send_keys('\b')
                    time.sleep(random.uniform(0.1, 0.2))
            
            print(f"✅ '{metin}' yazıldı")
            return True
            
        except Exception as e:
            print(f"❌ Yazma hatası: {e}")
            return False
    
    def rastgele_fare_hareketi(self):
        """Sayfada rastgele fare hareketleri"""
        try:
            hareket_sayisi = random.randint(2, 4)
            for _ in range(hareket_sayisi):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.driver.execute_script(f"window.scrollTo({x}, {y});")
                time.sleep(random.uniform(0.5, 1.0))
        except:
            pass
    
    def checkbox_isaretle(self):
        """Checkbox'ları işaretle"""
        print("\n☑️  Checkbox'lar işaretleniyor...")
        
        js_checkbox = """
        var checkboxlar = document.querySelectorAll("input[type='checkbox']");
        var isaret = [];
        
        checkboxlar.forEach(function(kutu, index) {
            if (!kutu.checked) {
                kutu.scrollIntoView({behavior: 'smooth', block: 'center'});
                setTimeout(function() {
                    kutu.click();
                    isaret.push(index);
                }, (index + 1) * 800);
            }
        });
        
        return {total: checkboxlar.length, isaretlendi: isaret};
        """
        
        sonuc = self.driver.execute_script(js_checkbox)
        
        if sonuc:
            print(f"✅ {len(sonuc.get('isaretlendi', []))} checkbox işaretlendi")
            time.sleep(len(sonuc.get('isaretlendi', [])) * 1)
        
        time.sleep(1)
    
    def hesap_ac(self, email, ad, soyad, sifre):
        """Ana hesap açma fonksiyonu"""
        try:
            print("🚀 Sahibinden'e gidiliyor...")
            
            # Önce ana sayfaya git (daha doğal)
            self.driver.get('https://www.sahibinden.com')
            time.sleep(random.uniform(4, 7))
            
            # Cloudflare kontrolü
            if not self.cloudflare_bekle(max_bekleme=40):
                print("❌ Ana sayfada Cloudflare engellenemedi!")
                print("⚠️  IP'nizi değiştirmeniz gerekebilir (VPN/Proxy)")
                return False
            
            # Ana sayfada biraz gezin (insan gibi)
            print("🏠 Ana sayfada geziniliyor...")
            self.rastgele_fare_hareketi()
            
            # Scroll yap
            for _ in range(random.randint(2, 4)):
                scroll_miktar = random.randint(300, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_miktar});")
                time.sleep(random.uniform(1, 2))
            
            # Şimdi kayıt sayfasına git
            print("\n📝 Kayıt sayfasına gidiliyor...")
            self.driver.get('https://secure.sahibinden.com/kayit/')
            time.sleep(random.uniform(4, 7))
            
            # Tekrar Cloudflare kontrolü
            if not self.cloudflare_bekle(max_bekleme=40):
                print("❌ Kayıt sayfasında Cloudflare engellenemedi!")
                print("💡 Öneriler:")
                print("   1. VPN/Proxy kullanın")
                print("   2. IP'nizi değiştirin (modem restart)")
                print("   3. 24 saat sonra tekrar deneyin")
                return False
            
            self.rastgele_fare_hareketi()
            
            # ============ ADIM 1: E-POSTA ============
            print(f"\n📧 E-posta giriliyor: {email}")
            
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='E-posta adresi']"))
            )
            
            basarili = self.insan_gibi_yaz(email_input, email)
            if not basarili:
                print("❌ Email yazılamadı!")
                return False
            
            time.sleep(random.uniform(2, 3))
            self.rastgele_fare_hareketi()
            
            # E-posta butonu
            print("\n🔘 E-posta butonu tıklanıyor...")
            email_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'E-posta ile hesap aç')]"))
            )
            
            self.actions.move_to_element(email_btn).pause(random.uniform(1, 2)).click().perform()
            print("✅ E-posta butonu tıklandı")
            
            # ============ ADIM 2: BİLGİ GİRİŞİ ============
            print("\n⏳ Yeni sayfa yükleniyor...")
            time.sleep(random.uniform(4, 6))
            
            # Tekrar Cloudflare kontrolü
            if "Tarayıcınızı kontrol ediyoruz" in self.driver.page_source:
                if not self.cloudflare_bekle(max_bekleme=40):
                    print("❌ Bilgi sayfasında Cloudflare engellenemedi!")
                    return False
            
            # Ad girişi
            ad_input = self.wait.until(EC.presence_of_element_located((By.ID, "name")))
            
            print("\n👤 Bilgiler dolduruluyor...")
            
            self.insan_gibi_yaz(ad_input, ad)
            time.sleep(random.uniform(1, 2))
            
            # Soyad
            soyad_input = self.driver.find_element(By.ID, "surname")
            self.insan_gibi_yaz(soyad_input, soyad)
            time.sleep(random.uniform(1, 2))
            
            # Şifre
            sifre_input = self.driver.find_element(By.ID, "password")
            self.insan_gibi_yaz(sifre_input, sifre)
            time.sleep(random.uniform(2, 3))
            
            # ============ ADIM 3: CHECKBOX'LAR ============
            print("\n☑️  Sözleşmeler okunuyor...")
            time.sleep(random.uniform(3, 5))
            
            self.checkbox_isaretle()
            time.sleep(random.uniform(2, 3))
            
            # ============ ADIM 4: HESAP AÇ ============
            print("\n🎯 Hesap Aç butonuna basılıyor...")
            
            js_hesap_ac = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.includes('Hesap Aç')) {
                    buttons[i].scrollIntoView({behavior: 'smooth', block: 'center'});
                    setTimeout(function() {
                        buttons[i].click();
                    }, 1000);
                    return true;
                }
            }
            return false;
            """
            
            sonuc = self.driver.execute_script(js_hesap_ac)
            if sonuc:
                print("🎉 Hesap Aç butonuna basıldı!")
            else:
                print("❌ Hesap Aç butonu bulunamadı!")
                return False
            
            # ============ ADIM 5: POPUP ============
            print("\n⏳ Popup bekleniyor...")
            time.sleep(random.uniform(3, 5))
            
            js_popup = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].textContent;
                if (text.includes('Devam') || text.includes('Doğru')) {
                    buttons[i].click();
                    return {success: true, text: text};
                }
            }
            return {success: false};
            """
            
            sonuc = self.driver.execute_script(js_popup)
            if sonuc and sonuc.get('success'):
                print(f"✅ Popup onaylandı: '{sonuc.get('text')}'")
            
            print("\n✅✅✅ İŞLEM TAMAMLANDI! ✅✅✅")
            
            return True
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def kapat(self):
        """Tarayıcıyı kapat"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔴 Tarayıcı kapatıldı")
            except:
                pass

# ============ KULLANIM ============
def main():
    # Hesap bilgileri
    EMAIL = "denemehesap66664@gmail.com"
    AD = "Mehmet"
    SOYAD = "Demir"
    SIFRE = "GucluSifre.123"
    
    print(f"\n{'='*60}")
    print(f"🛡️  CLOUDFLARE BYPASS BOT")
    print(f"{'='*60}")
    print(f"📧 Email  : {EMAIL}")
    print(f"👤 İsim   : {AD} {SOYAD}")
    print(f"{'='*60}\n")
    
    bot = CloudflareBypassBot()
    
    try:
        bot.hesap_ac(
            email=EMAIL,
            ad=AD,
            soyad=SOYAD,
            sifre=SIFRE
        )
    except Exception as e:
        print(f"❌ Ana hata: {e}")
    finally:
        input("\n⏸️  Tarayıcıyı kapatmak için Enter'a basın...")
        bot.kapat()

if __name__ == "__main__":
    main()