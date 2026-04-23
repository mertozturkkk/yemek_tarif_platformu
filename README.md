# 🍴 Yemek Tarif Platformu  
### Sistem Kullanım Kılavuzu (User Manual)

---

## 📌 1. Giriş

Bu doküman, Python programlama dili kullanılarak nesne tabanlı programlama (OOP) prensipleri doğrultusunda geliştirilen **Yemek Tarif Platformu** uygulamasının kullanımını açıklamak amacıyla hazırlanmıştır.

Sistem; kullanıcıların yemek tarifleri oluşturabildiği, güncelleyebildiği, değerlendirebildiği ve favorilerine ekleyebildiği konsol tabanlı bir platform sunmaktadır.

---

## 🧩 2. Sistem Genel Tanımı

Platform aşağıdaki temel işlevleri sağlar:

- 👤 Kullanıcı kayıt ve giriş işlemleri  
- 🍽️ Tarif ekleme, güncelleme ve silme  
- 🥕 Malzeme ve adım yönetimi  
- ⭐ Puanlama ve yorum sistemi  
- ❤️ Favori tarif listesi  
- 🔍 Arama ve filtreleme  
- 🏆 Popüler tariflerin listelenmesi  

---

## 🏗️ 3. Sistem Mimarisi

Sistem, nesne tabanlı programlama yaklaşımıyla aşağıdaki sınıflardan oluşmaktadır:

### 🔹 Malzeme
Bir tarifte kullanılan malzemeyi temsil eder.  
- Malzeme adı  
- Miktar  
- Kalori bilgisi  

### 🔹 Tarif
Yemek tarifini temsil eder.  
- Tarif adı, kategori, süre  
- Malzeme listesi  
- Pişirme adımları  
- Besin değerleri  
- Değerlendirmeler  

### 🔹 Kullanıcı
Platform kullanıcılarını temsil eder.  
- Kullanıcı bilgileri  
- Favori tarifler  
- Eklenen tarifler  

### 🔹 Değerlendirme
Tariflere verilen puan ve yorumları içerir.

### 🔹 Platform
Sistemin ana kontrol sınıfıdır.  
- Kullanıcı ve tarif yönetimi  
- Menü sistemi  
- İş mantığı  

---

## ⚙️ 4. Sistem Gereksinimleri

Projeyi çalıştırmak için:

- Python 3.x  
- Terminal / Komut satırı  

Ek bir kütüphane gerektirmez.

---

## ▶️ 5. Sistemin Çalıştırılması

Aşağıdaki komut ile program başlatılır:

```bash
python yemek.py
Program başlatıldığında:
Demo veriler yüklenir
Ana menü ekrana gelir
📋 6. Ana Menü
Sistem aşağıdaki seçenekleri sunar:
[1] Tüm tarifleri listele  
[2] Tarif ara  
[3] Filtreleme  
[4] Popüler tarifler  
[5] Tarif detayı görüntüle  
[6] Yeni tarif ekle  
[7] Puan / yorum ekle  
[8] Favori işlemleri  
[9] Güncelle / Sil  
[10] Giriş / Kayıt  
[11] Profil görüntüle  
[12] Kategori istatistikleri  
[0] Çıkış  
👤 7. Kullanım Senaryoları
🔐 7.1 Kullanıcı Kaydı ve Giriş
Kullanıcılar e-posta ile kayıt olur
Aynı e-posta tekrar kullanılamaz
Giriş sonrası kullanıcı aktif olur
🍳 7.2 Tarif Ekleme
Kullanıcılar aşağıdaki bilgileri girerek tarif oluşturur:
Tarif adı
Kategori
Süre
Porsiyon
Malzemeler
Pişirme adımları
✏️ 7.3 Tarif Güncelleme / Silme
Sadece tarif sahibi işlem yapabilir
Kısmi güncelleme mümkündür
🔍 7.4 Arama ve Filtreleme
Filtreleme kriterleri:
Kategori
Maksimum süre
Maksimum kalori
Zorluk seviyesi
Minimum puan
⭐ 7.5 Değerlendirme Sistemi
1–5 arası puan verilir
Yorum eklenebilir
Kullanıcı aynı tarifi yalnızca bir kez değerlendirebilir
❤️ 7.6 Favori Yönetimi
Tarif favorilere eklenir
Favoriler listelenir
Listeden çıkarılabilir
🏆 7.7 Popüler Tarifler
Tarifler şu kriterlere göre sıralanır:
Ortalama puan
Değerlendirme sayısı
💾 8. Veri Yönetimi
Sistem verileri geçici olarak bellekte tutulur:
Tarifler → Dictionary
Kullanıcılar → Dictionary
📌 Not: Kalıcı veri tabanı bulunmamaktadır.
⚠️ 9. Hata Yönetimi
Sistem aşağıdaki durumları kontrol eder:
Geçersiz puan girişleri
Aynı e-posta ile kayıt
Yetkisiz işlem denemeleri
Hatalı veri girişleri
🎯 10. Sonuç
Bu proje:
Nesne tabanlı programlama prensiplerini uygular
Modüler ve genişletilebilir yapı sunar
Konsol tabanlı kullanıcı etkileşimini içerir
🚀 11. Geliştirme Önerileri
GUI (Grafiksel arayüz) eklenmesi
Veritabanı entegrasyonu
Web tabanlı sistem geliştirme
Şifre güvenliği (hashleme)
👨‍💻 Geliştirici
Bu proje, eğitim amaçlı geliştirilmiş bir Python OOP uygulamasıdır.
