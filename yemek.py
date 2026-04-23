"""
============================================================
  PROJE 6: YEMEK TARİF PLATFORMU
  Nesne Tabanlı Programlama (OOP) - Python
============================================================

PROJE AÇIKLAMASI:
    Bu proje, kullanıcıların tarif ekleyebildiği, güncelleyebildiği,
    puan verebildiği, yorum yapabildiği ve favorilerine ekleyebildiği
    kapsamlı bir dijital yemek tarifi platformunu simüle eder.

SINIFLAR:
    - Malzeme     : Bir tarifin içerdiği malzeme bilgisi
    - Tarif        : Yemek tarifi (malzemeler, adımlar, puanlar)
    - Kullanici    : Platformdaki kullanıcı
    - Degerlendirme: Bir tarifte bırakılan puan + yorum
    - Platform     : Tüm sistemi yöneten ana sınıf

YENİ / EK ÖZELLİKLER:
    ✔ Adım adım pişirme talimatları
    ✔ Besin değeri takibi (kalori, protein, karbonhidrat, yağ)
    ✔ Favori tarif listesi
    ✔ Puan & yorum sistemi
    ✔ Kategori / süre / kalori filtreli arama
    ✔ Popüler tarifler sıralaması
    ✔ Detaylı konsol menüsü


"""

# ──────────────────────────────────────────────
# Standart kütüphane importları
# ──────────────────────────────────────────────
import uuid          # Benzersiz ID üretimi için
import datetime      # Tarih/saat işlemleri için
from typing import Optional  # Tip ipuçları için


# ════════════════════════════════════════════════════════════════
# SINIF 1 ─ Malzeme
# ════════════════════════════════════════════════════════════════
class Malzeme:
    """
    Bir tarifteki tek bir malzemeyi temsil eder.

    Özellikler:
        malzeme_adi (str) : Malzemenin adı (ör. "un", "süt")
        miktar      (str) : Miktarı ve birimi (ör. "2 su bardağı", "1 tatlı kaşığı")
        birim_kalori(float): 100 gram / 100 ml başına kalori (isteğe bağlı)
    """

    def __init__(self, malzeme_adi: str, miktar: str, birim_kalori: float = 0.0):
        # Malzemenin adı – zorunlu alan
        self.malzeme_adi = malzeme_adi
        # Miktar ve birimi tek string olarak tutuyoruz (ör. "200 gram")
        self.miktar = miktar
        # Besin hesabı için birim kalori (isteğe bağlı, varsayılan 0)
        self.birim_kalori = birim_kalori

    def __str__(self) -> str:
        """Malzemeyi okunabilir formatta gösterir."""
        return f"  • {self.miktar} {self.malzeme_adi}"

    def bilgi(self) -> dict:
        """Malzeme bilgisini sözlük olarak döner (JSON benzeri)."""
        return {
            "malzeme_adi": self.malzeme_adi,
            "miktar": self.miktar,
            "birim_kalori": self.birim_kalori
        }


# ════════════════════════════════════════════════════════════════
# SINIF 2 ─ Degerlendirme  (Puan + Yorum)
# ════════════════════════════════════════════════════════════════
class Degerlendirme:
    """
    Bir kullanıcının bir tarif için bıraktığı puan ve yorumu temsil eder.

    Özellikler:
        kullanici_id (str) : Değerlendirmeyi yapan kullanıcının ID'si
        puan         (int) : 1-5 arası yıldız puanı
        yorum        (str) : Opsiyonel metin yorumu
        tarih        (str) : Değerlendirme tarihi (otomatik atanır)
    """

    def __init__(self, kullanici_id: str, puan: int, yorum: str = ""):
        # Değerlendirmeyi kimin yaptığını takip ediyoruz
        self.kullanici_id = kullanici_id

        # Puan doğrulaması: 1-5 aralığı dışına çıkılmasını engelliyoruz
        if not (1 <= puan <= 5):
            raise ValueError("Puan 1 ile 5 arasında olmalıdır.")
        self.puan = puan

        self.yorum = yorum  # Boş da olabilir

        # Değerlendirme anının timestamp'i (ör. "2026-04-01 14:35")
        self.tarih = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def __str__(self) -> str:
        """Değerlendirmeyi yıldızlarla birlikte gösterir."""
        yildizlar = "★" * self.puan + "☆" * (5 - self.puan)
        yorum_goster = f' — "{self.yorum}"' if self.yorum else ""
        return f"[{self.tarih}] {yildizlar} (Kullanıcı: {self.kullanici_id}){yorum_goster}"


# ════════════════════════════════════════════════════════════════
# SINIF 3 ─ Tarif
# ════════════════════════════════════════════════════════════════
class Tarif:
    """
    Bir yemek tarifini tüm detaylarıyla temsil eder.

    Temel Özellikler (minimum proje gereksinimi):
        tarif_id          (str)        : Benzersiz UUID
        tarif_adi         (str)        : Yemeğin adı
        kategori          (str)        : Ana yemek, tatlı, çorba, vb.
        hazirlama_suresi  (int)        : Dakika cinsinden hazırlama süresi

    Ek Özellikler:
        malzemeler        (list)       : Malzeme nesnelerinin listesi
        adimlar           (list)       : Pişirme adımları (string listesi)
        degerlendirmeler  (list)       : Degerlendirme nesnelerinin listesi
        ekleyen_id        (str)        : Tarifi ekleyen kullanıcı ID'si
        eklenme_tarihi    (str)        : Tarihin platforma eklendiği tarih
        besin_degerleri   (dict)       : Kalori, protein, karbonhidrat, yağ
        zorluk_seviyesi   (str)        : Kolay / Orta / Zor
        porsiyon          (int)        : Kaç kişilik olduğu
    """

    def __init__(
        self,
        tarif_adi: str,
        kategori: str,
        hazirlama_suresi: int,
        ekleyen_id: str,
        zorluk_seviyesi: str = "Orta",
        porsiyon: int = 4
    ):
        # Her tarife otomatik benzersiz ID veriyoruz (UUID4 kısa versiyon)
        self.tarif_id = str(uuid.uuid4())[:8].upper()

        self.tarif_adi = tarif_adi
        self.kategori = kategori
        self.hazirlama_suresi = hazirlama_suresi  # dakika
        self.ekleyen_id = ekleyen_id
        self.zorluk_seviyesi = zorluk_seviyesi
        self.porsiyon = porsiyon

        # Eklenme anı otomatik kaydediliyor
        self.eklenme_tarihi = datetime.datetime.now().strftime("%Y-%m-%d")

        # Malzeme listesi – Malzeme nesneleri tutulur
        self.malzemeler: list[Malzeme] = []

        # Adım adım yapılış talimatları – string listesi
        self.adimlar: list[str] = []

        # Değerlendirme listesi – Degerlendirme nesneleri tutulur
        self.degerlendirmeler: list[Degerlendirme] = []

        # Besin değerleri sözlüğü (isteğe bağlı doldurulabilir)
        self.besin_degerleri: dict = {
            "kalori": 0,        # kcal
            "protein": 0,       # gram
            "karbonhidrat": 0,  # gram
            "yag": 0            # gram
        }

    # ── Malzeme İşlemleri ──────────────────────────────────────
    def malzeme_ekle(self, malzeme: "Malzeme") -> None:
        """
        Tarife yeni bir malzeme ekler.
        Aynı malzeme iki kez eklenirse uyarı verir.
        """
        # Aynı isimde malzeme var mı kontrol et (büyük/küçük harf duyarsız)
        mevcut_isimler = [m.malzeme_adi.lower() for m in self.malzemeler]
        if malzeme.malzeme_adi.lower() in mevcut_isimler:
            print(f"⚠  '{malzeme.malzeme_adi}' zaten malzeme listesinde mevcut.")
            return
        self.malzemeler.append(malzeme)

    def malzeme_cikar(self, malzeme_adi: str) -> bool:
        """
        İsme göre malzemeyi tariften çıkarır.
        Başarılı olursa True, bulunamazsa False döner.
        """
        for m in self.malzemeler:
            if m.malzeme_adi.lower() == malzeme_adi.lower():
                self.malzemeler.remove(m)
                return True
        return False

    # ── Adım İşlemleri ─────────────────────────────────────────
    def adim_ekle(self, adim_metni: str) -> None:
        """Pişirme talimatlarına sıradaki adımı ekler."""
        self.adimlar.append(adim_metni.strip())

    # ── Tarif Güncelleme ───────────────────────────────────────
    def tarif_guncelle(
        self,
        yeni_ad: Optional[str] = None,
        yeni_kategori: Optional[str] = None,
        yeni_sure: Optional[int] = None,
        yeni_zorluk: Optional[str] = None,
        yeni_porsiyon: Optional[int] = None
    ) -> None:
        """
        Tarifte güncelleme yapılmak istenen alanları değiştirir.
        Sadece None olmayan parametreler güncellenir (kısmi güncelleme).
        """
        if yeni_ad:
            self.tarif_adi = yeni_ad
        if yeni_kategori:
            self.kategori = yeni_kategori
        if yeni_sure is not None:
            self.hazirlama_suresi = yeni_sure
        if yeni_zorluk:
            self.zorluk_seviyesi = yeni_zorluk
        if yeni_porsiyon is not None:
            self.porsiyon = yeni_porsiyon
        print(f"✅ '{self.tarif_adi}' tarifi güncellendi.")

    # ── Besin Değerleri ────────────────────────────────────────
    def besin_degeri_guncelle(self, kalori: int = 0, protein: int = 0,
                               karbonhidrat: int = 0, yag: int = 0) -> None:
        """Tarife ait besin değerlerini (kalori, makro) günceller."""
        self.besin_degerleri["kalori"] = kalori
        self.besin_degerleri["protein"] = protein
        self.besin_degerleri["karbonhidrat"] = karbonhidrat
        self.besin_degerleri["yag"] = yag

    # ── Değerlendirme İşlemleri ────────────────────────────────
    def degerlendirme_ekle(self, deg: "Degerlendirme") -> None:
        """
        Tarife yeni bir puan/yorum ekler.
        Bir kullanıcı aynı tarifi yalnızca bir kez değerlendirebilir.
        """
        # Aynı kullanıcı daha önce puan verdiyse güncelle
        for i, d in enumerate(self.degerlendirmeler):
            if d.kullanici_id == deg.kullanici_id:
                self.degerlendirmeler[i] = deg
                print("🔄 Önceki değerlendirmeniz güncellendi.")
                return
        self.degerlendirmeler.append(deg)

    def ortalama_puan(self) -> float:
        """
        Tüm değerlendirmelerin ortalamasını döner.
        Değerlendirme yoksa 0.0 döner.
        """
        if not self.degerlendirmeler:
            return 0.0
        toplam = sum(d.puan for d in self.degerlendirmeler)
        return round(toplam / len(self.degerlendirmeler), 1)

    # ── Gösterim ───────────────────────────────────────────────
    def ozet_goster(self) -> None:
        """Tarifi kısa özet olarak ekrana basar (liste görünümü)."""
        puan_str = f"{self.ortalama_puan()}★" if self.degerlendirmeler else "Henüz puanlanmadı"
        print(
            f"  [{self.tarif_id}] {self.tarif_adi:<25} "
            f"| {self.kategori:<15} "
            f"| ⏱ {self.hazirlama_suresi} dk "
            f"| {self.zorluk_seviyesi:<6} "
            f"| {puan_str}"
        )

    def tam_bilgi_goster(self) -> None:
        """Tarifi tüm detaylarıyla ekrana basar."""
        ayrac = "═" * 60
        print(f"\n{ayrac}")
        print(f"  🍽  {self.tarif_adi.upper()}")
        print(ayrac)
        print(f"  ID           : {self.tarif_id}")
        print(f"  Kategori     : {self.kategori}")
        print(f"  Zorluk       : {self.zorluk_seviyesi}")
        print(f"  Süre         : {self.hazirlama_suresi} dakika")
        print(f"  Porsiyon     : {self.porsiyon} kişilik")
        print(f"  Ekleyen      : {self.ekleyen_id}")
        print(f"  Eklenme Tar. : {self.eklenme_tarihi}")
        print(f"  Ort. Puan    : {self.ortalama_puan()} / 5  ({len(self.degerlendirmeler)} değerlendirme)")

        # ─ Besin Değerleri
        b = self.besin_degerleri
        if any(b.values()):
            print(f"\n  📊 Besin Değerleri (porsiyon başına):")
            print(f"     Kalori: {b['kalori']} kcal | Protein: {b['protein']}g "
                  f"| Karbonhidrat: {b['karbonhidrat']}g | Yağ: {b['yag']}g")

        # ─ Malzemeler
        print(f"\n  🥕 Malzemeler ({len(self.malzemeler)} kalem):")
        if self.malzemeler:
            for m in self.malzemeler:
                print(m)
        else:
            print("  (malzeme girilmemiş)")

        # ─ Yapılış Adımları
        print(f"\n  📝 Yapılış ({len(self.adimlar)} adım):")
        if self.adimlar:
            for i, adim in enumerate(self.adimlar, start=1):
                print(f"  {i}. {adim}")
        else:
            print("  (adım girilmemiş)")

        # ─ Değerlendirmeler
        print(f"\n  💬 Değerlendirmeler:")
        if self.degerlendirmeler:
            for d in self.degerlendirmeler:
                print(f"  {d}")
        else:
            print("  (henüz değerlendirme yok)")

        print(ayrac)


# ════════════════════════════════════════════════════════════════
# SINIF 4 ─ Kullanıcı
# ════════════════════════════════════════════════════════════════
class Kullanici:
    """
    Platformdaki bir kullanıcıyı temsil eder.

    Özellikler:
        kullanici_id (str)  : Benzersiz UUID (otomatik)
        ad           (str)  : Kullanıcı görünen adı
        email        (str)  : E-posta adresi (login için)
        sifre        (str)  : Şifre (hash'lenmeden tutulur – demo amaçlı)
        favoriler    (list) : Favori tarif ID'lerinin listesi
        eklenen_tarif(list) : Bu kullanıcının eklediği tarif ID'leri
        aktif        (bool) : Hesap aktiflik durumu
    """

    def __init__(self, ad: str, email: str, sifre: str):
        self.kullanici_id = str(uuid.uuid4())[:8].upper()
        self.ad = ad
        self.email = email.lower().strip()
        self.sifre = sifre              # Gerçek projede hash'lenmelidir!
        self.favoriler: list[str] = []  # Favori tarif ID listesi
        self.eklenen_tarifler: list[str] = []  # Kullanıcının eklediği tariflerin ID'leri
        self.aktif = True
        self.kayit_tarihi = datetime.datetime.now().strftime("%Y-%m-%d")

    # ── Değerlendirme ──────────────────────────────────────────
    def tarif_degerlendir(self, tarif: "Tarif", puan: int, yorum: str = "") -> None:
        """
        Belirtilen tarife puan ve opsiyonel yorum ekler.
        Kendi tarifini değerlendirmeye izin verilmez.
        """
        # Kendi tarifine puan vermeyi engelle
        if tarif.ekleyen_id == self.kullanici_id:
            print("❌ Kendi tarifinizi değerlendiremezsiniz.")
            return

        try:
            deg = Degerlendirme(self.kullanici_id, puan, yorum)
            tarif.degerlendirme_ekle(deg)
            print(f"✅ '{tarif.tarif_adi}' tarifine {puan} puan verdiniz.")
        except ValueError as e:
            # Degerlendirme sınıfından gelen hata mesajını göster
            print(f"❌ Hata: {e}")

    # ── Favori İşlemleri ───────────────────────────────────────
    def favoriye_ekle(self, tarif: "Tarif") -> None:
        """Tarifi kullanıcının favori listesine ekler."""
        if tarif.tarif_id in self.favoriler:
            print(f"ℹ  '{tarif.tarif_adi}' zaten favorilerinizde.")
        else:
            self.favoriler.append(tarif.tarif_id)
            print(f"❤️  '{tarif.tarif_adi}' favorilere eklendi.")

    def favoriden_cikar(self, tarif_id: str) -> None:
        """Tarifi favori listesinden çıkarır."""
        if tarif_id in self.favoriler:
            self.favoriler.remove(tarif_id)
            print("💔 Tarif favorilerden kaldırıldı.")
        else:
            print("❌ Bu tarif favorilerinizde değil.")

    # ── Gösterim ───────────────────────────────────────────────
    def profil_goster(self) -> None:
        """Kullanıcı profil bilgilerini ekrana basar."""
        print(f"\n{'─'*40}")
        print(f"  👤 {self.ad}")
        print(f"  ID    : {self.kullanici_id}")
        print(f"  E-mail: {self.email}")
        print(f"  Kayıt : {self.kayit_tarihi}")
        print(f"  Tarif : {len(self.eklenen_tarifler)} tarif ekledi")
        print(f"  Favori: {len(self.favoriler)} tarif")
        print(f"{'─'*40}")

    def __str__(self) -> str:
        return f"{self.ad} ({self.kullanici_id})"


# ════════════════════════════════════════════════════════════════
# SINIF 5 ─ Platform  (Ana Yönetim Sınıfı)
# ════════════════════════════════════════════════════════════════
class Platform:
    """
    Tüm tarif platformunu yöneten merkezi sınıf.

    Bu sınıf aşağıdaki ana görevleri üstlenir:
        - Kullanıcı kayıt / giriş yönetimi
        - Tarif ekleme / silme / listeleme
        - Arama ve filtreleme
        - Popüler tarif sıralaması
        - Menü akışı (konsol arayüzü)

    Özellikler:
        tarifler (dict)    : {tarif_id: Tarif}
        kullanicilar (dict): {kullanici_id: Kullanici}
        aktif_kullanici    : Oturum açmış kullanıcı (None ise giriş yok)
    """

    def __init__(self, platform_adi: str = "LezzetDünyası"):
        self.platform_adi = platform_adi

        # Tüm tarifler tarif_id → Tarif eşlemesiyle sözlükte tutulur
        self.tarifler: dict[str, Tarif] = {}

        # Tüm kullanıcılar kullanici_id → Kullanici eşlemesiyle sözlükte tutulur
        self.kullanicilar: dict[str, Kullanici] = {}

        # Email → kullanici_id eşlemesi (hızlı giriş kontrolü için)
        self._email_index: dict[str, str] = {}

        # Oturum açmış kullanıcı referansı
        self.aktif_kullanici: Optional[Kullanici] = None

    # ════════════════════════════════════════════════════════════
    # KULLANICI YÖNETİMİ
    # ════════════════════════════════════════════════════════════
    def kullanici_kayit(self, ad: str, email: str, sifre: str) -> Optional[Kullanici]:
        """
        Yeni kullanıcı kaydı oluşturur.
        Aynı e-posta ile ikinci kayda izin verilmez.
        """
        email_lower = email.lower().strip()
        if email_lower in self._email_index:
            print("❌ Bu e-posta adresi zaten kayıtlı.")
            return None

        yeni_k = Kullanici(ad, email_lower, sifre)
        self.kullanicilar[yeni_k.kullanici_id] = yeni_k
        self._email_index[email_lower] = yeni_k.kullanici_id
        print(f"✅ Kayıt başarılı! Hoş geldiniz, {ad}. (ID: {yeni_k.kullanici_id})")
        return yeni_k

    def giris_yap(self, email: str, sifre: str) -> bool:
        """
        Kullanıcı girişi yapar.
        E-posta ve şifre eşleşirse aktif_kullanici güncellenir.
        """
        email_lower = email.lower().strip()
        if email_lower not in self._email_index:
            print("❌ Kullanıcı bulunamadı.")
            return False

        uid = self._email_index[email_lower]
        kullanici = self.kullanicilar[uid]

        if kullanici.sifre != sifre:
            print("❌ Şifre hatalı.")
            return False

        self.aktif_kullanici = kullanici
        print(f"✅ Giriş başarılı! Hoş geldiniz, {kullanici.ad}.")
        return True

    def cikis_yap(self) -> None:
        """Aktif kullanıcının oturumunu kapatır."""
        if self.aktif_kullanici:
            print(f"👋 Görüşürüz, {self.aktif_kullanici.ad}!")
        self.aktif_kullanici = None

    def _giris_gerekli(self) -> bool:
        """
        İşlem yapmak için giriş zorunluluğunu kontrol eden yardımcı metod.
        Giriş yapılmamışsa uyarı basar ve False döner.
        """
        if not self.aktif_kullanici:
            print("❌ Bu işlem için giriş yapmanız gerekiyor.")
            return False
        return True

    # ════════════════════════════════════════════════════════════
    # TARİF YÖNETİMİ
    # ════════════════════════════════════════════════════════════
    def tarif_ekle(self, tarif: Tarif) -> None:
        """
        Platforma yeni tarif ekler.
        Ekleyen kullanıcının eklenen_tarifler listesi güncellenir.
        """
        if not self._giris_gerekli():
            return

        self.tarifler[tarif.tarif_id] = tarif

        # Tarifi ekleyen kullanıcının profiline de kaydediyoruz
        self.aktif_kullanici.eklenen_tarifler.append(tarif.tarif_id)
        print(f"✅ '{tarif.tarif_adi}' tarifi platforma eklendi. (ID: {tarif.tarif_id})")

    def tarif_sil(self, tarif_id: str) -> bool:
        """
        Tarifi platformdan siler.
        Yalnızca tarifi ekleyen kullanıcı ya da admin silebilir.
        """
        if not self._giris_gerekli():
            return False

        if tarif_id not in self.tarifler:
            print("❌ Tarif bulunamadı.")
            return False

        tarif = self.tarifler[tarif_id]
        if tarif.ekleyen_id != self.aktif_kullanici.kullanici_id:
            print("❌ Sadece kendi tarifinizi silebilirsiniz.")
            return False

        del self.tarifler[tarif_id]
        print(f"🗑  '{tarif.tarif_adi}' tarifi silindi.")
        return True

    def tarif_guncelle_menu(self, tarif_id: str) -> None:
        """
        Var olan bir tarifi güncelleme akışı.
        Sadece tarifi ekleyen kullanıcı güncelleyebilir.
        """
        if not self._giris_gerekli():
            return

        if tarif_id not in self.tarifler:
            print("❌ Tarif bulunamadı.")
            return

        tarif = self.tarifler[tarif_id]
        if tarif.ekleyen_id != self.aktif_kullanici.kullanici_id:
            print("❌ Sadece kendi tarifinizi güncelleyebilirsiniz.")
            return

        # Hangi alanı güncellemek istediğini kullanıcıya sor
        print("\n--- Güncelleme Menüsü ---")
        print("1. Tarif adı")
        print("2. Kategori")
        print("3. Hazırlama süresi")
        print("4. Zorluk seviyesi")
        print("5. Porsiyon")
        secim = input("Güncellenecek alan: ").strip()

        guncellemeler = {}
        if secim == "1":
            guncellemeler["yeni_ad"] = input("Yeni ad: ")
        elif secim == "2":
            guncellemeler["yeni_kategori"] = input("Yeni kategori: ")
        elif secim == "3":
            try:
                guncellemeler["yeni_sure"] = int(input("Yeni süre (dk): "))
            except ValueError:
                print("❌ Geçersiz sayı.")
                return
        elif secim == "4":
            guncellemeler["yeni_zorluk"] = input("Yeni zorluk (Kolay/Orta/Zor): ")
        elif secim == "5":
            try:
                guncellemeler["yeni_porsiyon"] = int(input("Yeni porsiyon: "))
            except ValueError:
                print("❌ Geçersiz sayı.")
                return
        else:
            print("❌ Geçersiz seçim.")
            return

        tarif.tarif_guncelle(**guncellemeler)

    # ════════════════════════════════════════════════════════════
    # ARAMA VE FİLTRELEME
    # ════════════════════════════════════════════════════════════
    def tarif_ara(self, anahtar_kelime: str) -> list[Tarif]:
        """
        Tarif adında veya kategorisinde anahtar kelime araması yapar.
        Büyük/küçük harf duyarsız çalışır.
        Sonuçları liste olarak döner.
        """
        kw = anahtar_kelime.lower()
        sonuclar = [
            t for t in self.tarifler.values()
            if kw in t.tarif_adi.lower() or kw in t.kategori.lower()
        ]
        return sonuclar

    def filtrele(
        self,
        kategori: Optional[str] = None,
        maks_sure: Optional[int] = None,
        maks_kalori: Optional[int] = None,
        zorluk: Optional[str] = None,
        min_puan: Optional[float] = None
    ) -> list[Tarif]:
        """
        Çoklu kriter bazlı filtreleme.

        Parametreler:
            kategori   : Yemek kategorisi (ör. "Tatlı")
            maks_sure  : En fazla kaç dakika sürmeli
            maks_kalori: Porsiyon başına maksimum kalori
            zorluk     : "Kolay", "Orta" veya "Zor"
            min_puan   : Minimum ortalama yıldız puanı
        """
        sonuclar = list(self.tarifler.values())

        if kategori:
            sonuclar = [t for t in sonuclar if t.kategori.lower() == kategori.lower()]
        if maks_sure is not None:
            sonuclar = [t for t in sonuclar if t.hazirlama_suresi <= maks_sure]
        if maks_kalori is not None:
            sonuclar = [t for t in sonuclar if t.besin_degerleri["kalori"] <= maks_kalori]
        if zorluk:
            sonuclar = [t for t in sonuclar if t.zorluk_seviyesi.lower() == zorluk.lower()]
        if min_puan is not None:
            sonuclar = [t for t in sonuclar if t.ortalama_puan() >= min_puan]

        return sonuclar

    # ════════════════════════════════════════════════════════════
    # LİSTELEME VE RAPORLAMA
    # ════════════════════════════════════════════════════════════
    def tum_tarifleri_listele(self) -> None:
        """Platformdaki tüm tarifleri özet halinde listeler."""
        if not self.tarifler:
            print("📭 Platformda henüz tarif bulunmuyor.")
            return

        print(f"\n{'─'*80}")
        print(f"  Toplam {len(self.tarifler)} tarif")
        print(f"{'─'*80}")
        for t in self.tarifler.values():
            t.ozet_goster()
        print(f"{'─'*80}")

    def populer_tarifler(self, n: int = 5) -> list[Tarif]:
        """
        En yüksek ortalama puana sahip ilk N tarifi döner.
        Puanı eşit olan tarifler değerlendirme sayısına göre sıralanır.
        """
        sirali = sorted(
            self.tarifler.values(),
            key=lambda t: (t.ortalama_puan(), len(t.degerlendirmeler)),
            reverse=True
        )
        return sirali[:n]

    def favori_tarifleri_goster(self) -> None:
        """Aktif kullanıcının favori tariflerini listeler."""
        if not self._giris_gerekli():
            return

        favori_ids = self.aktif_kullanici.favoriler
        if not favori_ids:
            print("💔 Henüz favori tarifiniz yok.")
            return

        print(f"\n❤️  {self.aktif_kullanici.ad} – Favori Tarifler")
        print(f"{'─'*60}")
        for fid in favori_ids:
            if fid in self.tarifler:
                self.tarifler[fid].ozet_goster()
            else:
                print(f"  [{fid}] (Bu tarif silinmiş)")
        print(f"{'─'*60}")

    def kategori_istatistigi(self) -> dict:
        """
        Her kategoride kaç tarif olduğunu döner.
        Örnek: {"Tatlı": 5, "Çorba": 3, "Ana Yemek": 10}
        """
        istatistik: dict[str, int] = {}
        for t in self.tarifler.values():
            istatistik[t.kategori] = istatistik.get(t.kategori, 0) + 1
        return istatistik

    # ════════════════════════════════════════════════════════════
    # KONSOL MENÜSÜ  (Ana Arayüz)
    # ════════════════════════════════════════════════════════════
    def _baslik_yazdir(self) -> None:
        """Uygulamanın başlık banner'ını ekrana basar."""
        print("\n" + "═" * 60)
        print(f"  🍴  {self.platform_adi.upper()}  🍴")
        print("  Yemek Tarif Platformu  –  OOP Python Projesi")
        print("═" * 60)

    def _ana_menu_yazdir(self) -> None:
        """Ana menü seçeneklerini ekrana basar."""
        print("\n┌─── ANA MENÜ " + "─" * 40)
        if self.aktif_kullanici:
            print(f"│  👤 {self.aktif_kullanici.ad} olarak oturum açık")
        else:
            print("│  🔒 Giriş yapılmamış")
        print("├" + "─" * 53)
        print("│  [1] Tüm tarifleri listele")
        print("│  [2] Tarif ara")
        print("│  [3] Tarifleri filtrele")
        print("│  [4] Popüler tarifler")
        print("│  [5] Tarif detayı görüntüle")
        print("├" + "─" * 53)
        print("│  [6] Yeni tarif ekle")
        print("│  [7] Tarifleme puan/yorum ekle")
        print("│  [8] Favorilere ekle / Favorilerimi gör")
        print("│  [9] Tarif güncelle / Sil")
        print("├" + "─" * 53)
        print("│  [10] Giriş yap / Kayıt ol / Çıkış")
        print("│  [11] Profil göster")
        print("│  [12] Kategori istatistikleri")
        print("│  [0] Programdan çık")
        print("└" + "─" * 53)

    # ─── Yardımcı giriş metodları ──────────────────────────────
    def _giris_kayit_menu(self) -> None:
        """Giriş / kayıt alt menüsü."""
        print("\n  [1] Giriş yap")
        print("  [2] Yeni kayıt")
        print("  [3] Oturumu kapat")
        secim = input("  Seçim: ").strip()

        if secim == "1":
            email = input("  E-posta: ").strip()
            sifre = input("  Şifre  : ").strip()
            self.giris_yap(email, sifre)

        elif secim == "2":
            ad    = input("  Ad    : ").strip()
            email = input("  E-posta: ").strip()
            sifre = input("  Şifre  : ").strip()
            k = self.kullanici_kayit(ad, email, sifre)
            if k:
                # Kayıt sonrası otomatik giriş
                self.aktif_kullanici = k

        elif secim == "3":
            self.cikis_yap()

    def _tarif_ekle_menu(self) -> None:
        """Interaktif tarif ekleme akışı."""
        if not self._giris_gerekli():
            return

        print("\n--- Yeni Tarif Ekle ---")
        ad      = input("Tarif adı     : ").strip()
        kategori= input("Kategori      : ").strip()
        try:
            sure    = int(input("Süre (dk)     : ").strip())
            porsiyon= int(input("Porsiyon      : ").strip())
        except ValueError:
            print("❌ Geçersiz sayı.")
            return
        zorluk  = input("Zorluk (Kolay/Orta/Zor): ").strip()

        # Tarif nesnesi oluştur
        yeni_tarif = Tarif(
            tarif_adi=ad,
            kategori=kategori,
            hazirlama_suresi=sure,
            ekleyen_id=self.aktif_kullanici.kullanici_id,
            zorluk_seviyesi=zorluk,
            porsiyon=porsiyon
        )

        # Malzemeleri al
        print("\nMalzeme girin (bitirmek için boş bırakın):")
        while True:
            malzeme_adi = input("  Malzeme adı (boş = bitir): ").strip()
            if not malzeme_adi:
                break
            miktar = input(f"  {malzeme_adi} miktarı: ").strip()
            yeni_tarif.malzeme_ekle(Malzeme(malzeme_adi, miktar))

        # Pişirme adımlarını al
        print("\nPişirme adımı girin (bitirmek için boş bırakın):")
        adim_no = 1
        while True:
            adim = input(f"  Adım {adim_no}: ").strip()
            if not adim:
                break
            yeni_tarif.adim_ekle(adim)
            adim_no += 1

        # Besin değerleri (isteğe bağlı)
        b_giris = input("\nBesin değeri girmek ister misiniz? (e/h): ").strip().lower()
        if b_giris == "e":
            try:
                kalori  = int(input("  Kalori (kcal): "))
                protein = int(input("  Protein (g)  : "))
                karb    = int(input("  Karbonhidrat (g): "))
                yag     = int(input("  Yağ (g)      : "))
                yeni_tarif.besin_degeri_guncelle(kalori, protein, karb, yag)
            except ValueError:
                print("⚠  Besin değerleri atlandı (geçersiz giriş).")

        self.tarif_ekle(yeni_tarif)

    def _degerlendirme_menu(self) -> None:
        """Tarife puan ve yorum ekleme akışı."""
        if not self._giris_gerekli():
            return

        tarif_id = input("Değerlendirilecek tarif ID: ").strip().upper()
        if tarif_id not in self.tarifler:
            print("❌ Tarif bulunamadı.")
            return

        try:
            puan = int(input("Puan (1-5): ").strip())
        except ValueError:
            print("❌ Geçersiz puan.")
            return

        yorum = input("Yorum (boş bırakabilirsiniz): ").strip()
        self.aktif_kullanici.tarif_degerlendir(self.tarifler[tarif_id], puan, yorum)

    def _favori_menu(self) -> None:
        """Favori ekleme/gösterme alt menüsü."""
        if not self._giris_gerekli():
            return
        print("\n  [1] Favorilere ekle")
        print("  [2] Favorilerimden çıkar")
        print("  [3] Favorilerimi göster")
        secim = input("  Seçim: ").strip()

        if secim == "1":
            tid = input("Tarif ID: ").strip().upper()
            if tid in self.tarifler:
                self.aktif_kullanici.favoriye_ekle(self.tarifler[tid])
            else:
                print("❌ Tarif bulunamadı.")
        elif secim == "2":
            tid = input("Tarif ID: ").strip().upper()
            self.aktif_kullanici.favoriden_cikar(tid)
        elif secim == "3":
            self.favori_tarifleri_goster()

    def _filtreleme_menu(self) -> None:
        """Filtreli tarif arama menüsü."""
        print("\n--- Filtreleme Menüsü ---")
        print("(Boş bırakılan filtreler uygulanmaz)")

        kategori  = input("Kategori         : ").strip() or None
        sure_str  = input("Maks. süre (dk)  : ").strip()
        kalori_str= input("Maks. kalori     : ").strip()
        zorluk    = input("Zorluk           : ").strip() or None
        puan_str  = input("Min. puan (1-5)  : ").strip()

        maks_sure  = int(sure_str)   if sure_str.isdigit()  else None
        maks_kalori= int(kalori_str) if kalori_str.isdigit() else None
        min_puan = None
        if puan_str:
            try:
                min_puan = float(puan_str)
            except ValueError:
                print("⚠ Geçersiz puan girişi! Puan filtresi yoksayıldı.")

        sonuclar = self.filtrele(kategori, maks_sure, maks_kalori, zorluk, min_puan)

        print(f"\n🔍 {len(sonuclar)} sonuç bulundu:")
        for t in sonuclar:
            t.ozet_goster()

    # ─── Ana Döngü ─────────────────────────────────────────────
    def calistir(self) -> None:
        """
        Uygulamanın ana döngüsü.
        Kullanıcı '0' girene kadar menüyü tekrar gösterir.
        """
        self._baslik_yazdir()

        while True:
            self._ana_menu_yazdir()
            secim = input("\nSeçiminiz: ").strip()

            # ── 1: Tüm tarifleri listele
            if secim == "1":
                self.tum_tarifleri_listele()

            # ── 2: Arama
            elif secim == "2":
                kw = input("Arama kelimesi: ").strip()
                sonuclar = self.tarif_ara(kw)
                print(f"🔍 '{kw}' için {len(sonuclar)} sonuç:")
                for t in sonuclar:
                    t.ozet_goster()

            # ── 3: Filtrele
            elif secim == "3":
                self._filtreleme_menu()

            # ── 4: Popüler
            elif secim == "4":
                print("\n🏆 Popüler Tarifler (Top 5):")
                for i, t in enumerate(self.populer_tarifler(5), 1):
                    print(f"  {i}. ", end="")
                    t.ozet_goster()

            # ── 5: Detay görüntüle
            elif secim == "5":
                tid = input("Tarif ID: ").strip().upper()
                if tid in self.tarifler:
                    self.tarifler[tid].tam_bilgi_goster()
                else:
                    print("❌ Tarif bulunamadı.")

            # ── 6: Tarif ekle
            elif secim == "6":
                self._tarif_ekle_menu()

            # ── 7: Değerlendirme
            elif secim == "7":
                self._degerlendirme_menu()

            # ── 8: Favori
            elif secim == "8":
                self._favori_menu()

            # ── 9: Güncelle / Sil
            elif secim == "9":
                print("\n  [1] Güncelle")
                print("  [2] Sil")
                alt_secim = input("  Seçim: ").strip()
                tid = input("Tarif ID: ").strip().upper()
                if alt_secim == "1":
                    self.tarif_guncelle_menu(tid)
                elif alt_secim == "2":
                    self.tarif_sil(tid)

            # ── 10: Giriş/Kayıt/Çıkış
            elif secim == "10":
                self._giris_kayit_menu()

            # ── 11: Profil
            elif secim == "11":
                if self._giris_gerekli():
                    self.aktif_kullanici.profil_goster()

            # ── 12: Kategori istatistikleri
            elif secim == "12":
                stats = self.kategori_istatistigi()
                print("\n📊 Kategori İstatistikleri:")
                for kat, adet in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    print(f"  {kat:<20}: {adet} tarif")

            # ── 0: Çıkış
            elif secim == "0":
                print("\n👋 İyi yemekler! Görüşürüz.\n")
                break

            else:
                print("❌ Geçersiz seçim, tekrar deneyin.")


# ════════════════════════════════════════════════════════════════
# DEMO VERİSİ – Sistemi hazır verilerle başlatır
# ════════════════════════════════════════════════════════════════
def demo_verisi_yukle(platform: Platform) -> None:
    """
    Geliştirme/test amaçlı hazır kullanıcı ve tarif verileri yükler.
    Gerçek uygulamada bu veriler veritabanından gelir.
    """
    print("⏳ Demo verisi yükleniyor...", end=" ")

    # ─ Kullanıcılar
    ayse = platform.kullanici_kayit("Ayşe Kaya", "ayse@mail.com", "1234")
    mehmet = platform.kullanici_kayit("Mehmet Yılmaz", "mehmet@mail.com", "5678")

    # ─ Ayşe ile giriş yap
    platform.aktif_kullanici = ayse

    # ─ Tarif 1: Mercimek Çorbası
    corba = Tarif("Mercimek Çorbası", "Çorba", 35, ayse.kullanici_id, "Kolay", 6)
    corba.malzeme_ekle(Malzeme("Kırmızı mercimek", "2 su bardağı", 352))
    corba.malzeme_ekle(Malzeme("Soğan", "1 adet"))
    corba.malzeme_ekle(Malzeme("Havuç", "1 adet"))
    corba.malzeme_ekle(Malzeme("Zeytinyağı", "3 yemek kaşığı", 884))
    corba.malzeme_ekle(Malzeme("Tuz", "1 tatlı kaşığı"))
    corba.adim_ekle("Soğan ve havucu yemeklik doğrayın, zeytinyağında kavurun.")
    corba.adim_ekle("Yıkanmış mercimeği ekleyin, 10 dk daha kavurun.")
    corba.adim_ekle("Üzerini geçecek kadar su ekleyip 20 dk haşlayın.")
    corba.adim_ekle("Blenderdan geçirip tuz ile tatlandırın.")
    corba.besin_degeri_guncelle(kalori=180, protein=12, karbonhidrat=28, yag=4)
    platform.tarif_ekle(corba)

    # ─ Tarif 2: Çikolatalı Sufle
    sufle = Tarif("Çikolatalı Sufle", "Tatlı", 25, ayse.kullanici_id, "Orta", 4)
    sufle.malzeme_ekle(Malzeme("Bitter çikolata", "200 gram", 546))
    sufle.malzeme_ekle(Malzeme("Tereyağı", "100 gram", 717))
    sufle.malzeme_ekle(Malzeme("Yumurta", "3 adet", 155))
    sufle.malzeme_ekle(Malzeme("Toz şeker", "50 gram"))
    sufle.malzeme_ekle(Malzeme("Un", "30 gram"))
    sufle.adim_ekle("Çikolata ve tereyağını benmari usulü eritin.")
    sufle.adim_ekle("Yumurta ve şekeri köpük kıvamına gelinceye kadar çırpın.")
    sufle.adim_ekle("Çikolatalı karışımı yavaşça yumurtalıya katın, unu ekleyin.")
    sufle.adim_ekle("Yağlanmış kalıplara döküp 200°C fırında 12 dk pişirin.")
    sufle.besin_degeri_guncelle(kalori=420, protein=8, karbonhidrat=35, yag=28)
    platform.tarif_ekle(sufle)

    # ─ Tarif 3: Tavuk Izgara
    platform.aktif_kullanici = mehmet
    izgara = Tarif("Tavuk Izgara", "Ana Yemek", 40, mehmet.kullanici_id, "Kolay", 2)
    izgara.malzeme_ekle(Malzeme("Tavuk göğsü", "2 adet (300g)"))
    izgara.malzeme_ekle(Malzeme("Zeytinyağı", "2 yemek kaşığı"))
    izgara.malzeme_ekle(Malzeme("Sarımsak", "2 diş"))
    izgara.malzeme_ekle(Malzeme("Kekik", "1 tatlı kaşığı"))
    izgara.malzeme_ekle(Malzeme("Tuz, karabiber", "Yeterince"))
    izgara.adim_ekle("Tavukları limon suyu, sarımsak ve baharatlarla 20 dk marine edin.")
    izgara.adim_ekle("Izgarayı iyice ısıtın, her iki tarafı 8'er dk pişirin.")
    izgara.adim_ekle("5 dk dinlendirip servis edin.")
    izgara.besin_degeri_guncelle(kalori=280, protein=42, karbonhidrat=2, yag=12)
    platform.tarif_ekle(izgara)

    # ─ Değerlendirmeler
    platform.aktif_kullanici = mehmet
    mehmet.tarif_degerlendir(corba, 5, "Muhteşem, tam kıvamında!")
    mehmet.tarif_degerlendir(sufle, 4, "Harika ama biraz tatlı geldi.")

    platform.aktif_kullanici = ayse
    ayse.tarif_degerlendir(izgara, 5, "Çok lezzetli, tavsiye ederim!")

    # Aktif kullanıcıyı sıfırla
    platform.aktif_kullanici = None
    print("✅ Hazır!\n")


# ════════════════════════════════════════════════════════════════
# PROGRAM GİRİŞ NOKTASI
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Platform nesnesini oluştur
    platform = Platform("LezzetDünyası")

    # Demo verisini yükle (test için – isteğe bağlı kaldırılabilir)
    demo_verisi_yukle(platform)

    # Konsol menüsünü başlat
    platform.calistir()