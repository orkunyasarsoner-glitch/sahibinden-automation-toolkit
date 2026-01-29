from DrissionPage import ChromiumPage, ChromiumOptions
import time
import random

class InsanGibiBot:
    def __init__(self):
        self.co = ChromiumOptions()
        self.insan_gibi_ayarlar()
        self.page = ChromiumPage(addr_or_opts=self.co)
    
    def insan_gibi_ayarlar(self):
        """Tarayıcıyı gerçek kullanıcı gibi yapılandır"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        ]
        self.co.set_user_agent(random.choice(user_agents))
        self.co.set_argument('--disable-blink-features=AutomationControlled')
        self.co.set_argument('--disable-dev-shm-usage')
        self.co.set_argument('--no-sandbox')
        self.co.set_argument('--window-size=1920,1080')
        self.co.set_argument('--lang=tr-TR')
    
    def insan_gibi_yaz(self, element_selector, metin):
        """İnsan gibi yazma - değişken hızlarda"""
        eleman = self.page.ele(element_selector)
        if not eleman:
            print(f"❌ Element bulunamadı: {element_selector}")
            return False
        
        # Elemana tıkla
        try:
            self.page.actions.move_to(eleman).wait(random.uniform(0.3, 0.7)).click()
        except:
            eleman.click()
        
        time.sleep(random.uniform(0.2, 0.5))
        
        # Önce temizle
        eleman.clear()
        time.sleep(random.uniform(0.1, 0.3))
        
        # Harfleri yaz
        for i, harf in enumerate(metin):
            self.page.actions.type(harf)
            
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
                self.page.actions.type(yanlis_harf)
                time.sleep(random.uniform(0.1, 0.2))
                self.page.actions.type('\b')
                time.sleep(random.uniform(0.1, 0.2))
        
        print(f"✅ '{metin}' yazıldı")
        return True
    
    def rastgele_sayfa_hareketi(self):
        """Sayfada rastgele fare hareketleri"""
        hareket_sayisi = random.randint(1, 3)
        for _ in range(hareket_sayisi):
            x = random.randint(300, 1000)
            y = random.randint(200, 600)
            try:
                self.page.actions.move_to((x, y))
            except:
                pass
            time.sleep(random.uniform(0.3, 0.8))
    
    def sayfa_oku_gibi_yap(self):
        """Sayfayı okuyor gibi yap"""
        print("📖 Sayfa okunuyor...")
        time.sleep(random.uniform(2, 4))
        self.rastgele_sayfa_hareketi()
    
    def checkbox_isaretle(self):
        """Checkbox'ları JS ile işaretle"""
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
        
        sonuc = self.page.run_js(js_checkbox)
        
        if sonuc:
            print(f"✅ {len(sonuc.get('isaretlendi', []))} checkbox işaretlendi")
            time.sleep(len(sonuc.get('isaretlendi', [])) * 1)
        
        time.sleep(1)
        checkboxlar = self.page.eles('tag:input@type=checkbox')
        
        for i, cb in enumerate(checkboxlar):
            if not cb.states.is_checked:
                try:
                    cb.click()
                    time.sleep(random.uniform(0.3, 0.7))
                except:
                    pass
    
    def hesap_ac(self, email, ad, soyad, sifre):
        """Ana hesap açma fonksiyonu"""
        try:
            print("🚀 Sahibinden'e gidiliyor...")
            self.page.get('https://secure.sahibinden.com/kayit/')
            
            time.sleep(random.uniform(2, 4))
            self.rastgele_sayfa_hareketi()
            
            # ============ ADIM 1: E-POSTA ============
            print(f"\n📧 E-posta giriliyor: {email}")
            
            email_input = self.page.ele('@placeholder=E-posta adresi')
            if email_input:
                email_input.clear()
                time.sleep(0.3)
            
            basarili = self.insan_gibi_yaz('@placeholder=E-posta adresi', email)
            if not basarili:
                print("❌ Email yazılamadı!")
                return False
            
            time.sleep(random.uniform(1, 2))
            self.rastgele_sayfa_hareketi()
            
            print("\n🔘 E-posta butonu tıklanıyor...")
            btn = self.page.ele('text:E-posta ile hesap aç')
            if btn:
                try:
                    self.page.actions.move_to(btn).wait(random.uniform(0.5, 1)).click()
                except:
                    btn.click()
                print("✅ E-posta butonu tıklandı")
            else:
                print("❌ E-posta butonu bulunamadı!")
                return False
            
            # ============ ADIM 2: BİLGİ GİRİŞİ ============
            print("\n⏳ Yeni sayfa yükleniyor...")
            time.sleep(random.uniform(3, 5))
            
            if not self.page.ele('#name'):
                print("❌ Sayfa yüklenemedi!")
                return False
            
            self.sayfa_oku_gibi_yap()
            
            print("\n👤 Bilgiler dolduruluyor...")
            
            if self.page.ele('#name'):
                self.insan_gibi_yaz('#name', ad)
                time.sleep(random.uniform(0.5, 1))
            
            if self.page.ele('#surname'):
                self.insan_gibi_yaz('#surname', soyad)
                time.sleep(random.uniform(0.5, 1))
            
            if self.page.ele('#password'):
                self.insan_gibi_yaz('#password', sifre)
                time.sleep(random.uniform(1, 2))
            
            # ============ ADIM 3: CHECKBOX'LAR ============
            print("\n☑️  Sözleşmeler okunuyor...")
            time.sleep(random.uniform(2, 3))
            
            self.checkbox_isaretle()
            
            time.sleep(random.uniform(1, 2))
            
            # ============ ADIM 4: HESAP AÇ ============
            print("\n🎯 Hesap Aç butonuna basılıyor...")
            
            js_hesap_ac = """
            var buttons = document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.includes('Hesap Aç')) {
                    buttons[i].scrollIntoView({behavior: 'smooth', block: 'center'});
                    setTimeout(function() {
                        buttons[i].click();
                    }, 500);
                    return true;
                }
            }
            return false;
            """
            
            sonuc = self.page.run_js(js_hesap_ac)
            if sonuc:
                print("🎉 Hesap Aç butonuna basıldı!")
            else:
                print("❌ Hesap Aç butonu bulunamadı!")
                return False
            
            # ============ ADIM 5: POPUP ============
            print("\n⏳ Popup bekleniyor...")
            time.sleep(random.uniform(2, 4))
            
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
            
            sonuc = self.page.run_js(js_popup)
            if sonuc and sonuc.get('success'):
                print(f"✅ Popup onaylandı: '{sonuc.get('text')}'")
            
            print("\n✅✅✅ İŞLEM TAMAMLANDI! ✅✅✅")
            
            # Captcha kontrolü
            time.sleep(2)
            if self.page.ele('tag:iframe@title^=reCAPTCHA') or self.page.ele('css:.g-recaptcha'):
                print("\n⚠️  CAPTCHA ALGILANDI!")
                print("Lütfen manuel olarak captcha'yı çözün...")
                input("Captcha çözüldükten sonra Enter'a basın...")
            
            return True
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            import traceback
            traceback.print_exc()
            return False

# ============ KULLANIM ============
def main():
    # ÖNEMLİ: Buraya kendi bilgilerinizi yazın
    EMAIL = "denemehesap99999@gmail.com"  
    AD = "Mehmet"
    SOYAD = "Demir"
    SIFRE = "GucluSifre.123"
    
    print(f"\n{'='*60}")
    print(f"🤖 SAHİBİNDEN HESAP AÇMA BOTU")
    print(f"{'='*60}")
    print(f"📧 Email  : {EMAIL}")
    print(f"👤 İsim   : {AD} {SOYAD}")
    print(f"{'='*60}\n")
    
    bot = InsanGibiBot()
    bot.hesap_ac(
        email=EMAIL,
        ad=AD,
        soyad=SOYAD,
        sifre=SIFRE
    )
    
    input("\n⏸️  Tarayıcıyı kapatmak için Enter'a basın...")
    bot.page.quit()

if __name__ == "__main__":
    main()