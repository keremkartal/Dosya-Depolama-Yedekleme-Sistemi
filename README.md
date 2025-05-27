# Dosya Depolama / Yedekleme Sistemi

Bu proje, bir dosya depolama ve yedekleme sisteminin temel işlevlerini yerine getiren bir **Python** uygulamasıdır. Proje kapsamında:

- Farklı rol ve yetkilere sahip kullanıcı profilleri oluşturulabilmesi
- Takım kavramı ile kullanıcılar arası dosya paylaşımı
- Parola değiştirme talep/onay mekanizması
- Dosya ekleme, listeleme ve paylaşma
- (Gelecekte genişletilebilecek şekilde) Log işlemleri ve anormal durum tespiti için altyapı

gibi işlemler desteklenmektedir.



## Özellikler

1. **Kullanıcı Profilleri:**
   - Bireysel Kullanıcı
   - Sistem Yöneticisi

2. **Kimlik Doğrulama:**
   - Üye olma (Bireysel Kullanıcı veya Sistem Yöneticisi olarak)
   - Giriş yapma (Kullanıcı adı ve şifre kontrolü)
   - Şifre değiştirme talebi ve yönetici onayı sonrasında şifre güncelleme

3. **Dosya Yönetimi:**
   - Yerel dosyaları sisteme yükleme
   - Sahip olunan dosyaları görüntüleme
   - Dosyaları takım üyeleriyle paylaşma

4. **Takım Yönetimi:**
   - Yeni takım oluşturma
   - Takımlara davet gönderme
   - Davetleri kabul etme / reddetme

5. **Bildirim Sistemi:**
   - Takıma davet bildirimleri
   - Parola değiştirme istek/onay bildirimleri

6. **Veritabanı (SQLite) Entegrasyonu:**
   - Kullanıcı bilgileri ve şifrelerin saklanması (basit örnek, şifreleme entegrasyonu eklenebilir)
   - Dosyaların sistemdeki yolu ve sahiplik bilgileri
   - Takım bilgileri ve üye ilişkileri

7. **Genişletilebilir Yapı:**
   - Log dosyaları oluşturmak, 
   - Anomali tespiti (örn. çok sayıda başarısız giriş denemesi),
   - Dosya yedekleme / senkronizasyon işlemleri vb. eklenmeye hazır iskelet kod yapısı.

---

## Kullanılan Teknolojiler

- **Dil:** Python 3 (Tkinter kütüphanesi kullanılarak masaüstü arayüzü oluşturuldu)
- **Veritabanı:** SQLite (Python `sqlite3` modülü)
- **Arayüz:** Tkinter

---

## Gereksinimler

- Python 3.7+ (Tercihen 3.9 veya üstü)
- Tkinter (Python ile birlikte genelde varsayılan gelir)
- SQLite (Python’da `sqlite3` paketi ile birlikte kullanılır, ek bir kurulum gerektirmez)

> **Not:** Tkinter bazı işletim sistemlerinde ekstra paket olarak kurulabiliyor. Çoğu Linux dağıtımında `python3-tk` paketini yüklemeniz gerekebilir.

---

## Kurulum ve Çalıştırma

1. Bu projeyi GitHub reposundan klonlayın veya `.zip` olarak indirip açın:
   ```bash
   git clone <repo-url>
   cd <klonlanan-dizin>
   ```

2. Gerekli Python sürümüne ve Tkinter’a sahip olduğunuzdan emin olun.

3. Uygulamayı çalıştırmak için ana Python dosyasını (örneğin `main.py` veya bu örnekte verdiğiniz dosya adı) çalıştırın:
   ```bash
   python main.py
   ```

4. Uygulama açıldığında karşınıza ilk olarak **Üye Ol** veya **Giriş Yap** butonlarını içeren bir pencere gelecektir.

---

## Veritabanı Yapısı

Proje kapsamında `sqlite3` veritabanında şu tablolar kullanılmaktadır:

1. **kullanicilar** 
   | Alan               | Açıklama                                                               |
   |--------------------|------------------------------------------------------------------------|
   | id (INTEGER)       | Otomatik artan, birincil anahtar (PRIMARY KEY)                         |
   | kullanici_adi (TEXT, UNIQUE) | Kullanıcı adını saklar, benzersiz olması zorunludur          |
   | sifre (TEXT)       | Kullanıcının şifresini saklar (örnek uygulamada düz metin, istenirse şifrelenebilir) |
   | rol (TEXT)         | "Bireysel Kullanıcı" veya "Sistem Yöneticisi"                          |
   | bildirimler (TEXT) | JSON formatında bildirim listesi                                       |
   | parolaistek (INTEGER) | Parola değiştirme isteğinin onay durumu (0 veya 1)                  |

2. **dosyalar**
   | Alan               | Açıklama                                                               |
   |--------------------|------------------------------------------------------------------------|
   | id (INTEGER)       | Otomatik artan, birincil anahtar                                       |
   | dosya_adi (TEXT)   | Dosyanın adı                                                           |
   | dosya_yolu (TEXT)  | Dosyanın lokal disk üzerinde bulunduğu tam yol                         |
   | erisebilen_kullanici_id (TEXT) | Hangi kullanıcının (veya kullanıcıların) bu dosyaya erişebildiği bilgisi |

3. **takimlar**
   | Alan               | Açıklama                                                               |
   |--------------------|------------------------------------------------------------------------|
   | id (INTEGER)       | Otomatik artan, birincil anahtar                                       |
   | takim_adi (TEXT)   | Takım adı, benzersiz (UNIQUE)                                          |

4. **takim_uyeleri**
   | Alan               | Açıklama                                                               |
   |--------------------|------------------------------------------------------------------------|
   | takim_id (INTEGER) | Takım ID’si                                                            |
   | kullanici_id (INTEGER) | Kullanıcı ID’si                                                    |

> **Not:** Projenin ilerleyen aşamalarında **log** tabloları veya log dosyaları oluşturmak, anomali tespiti gibi ek tablolar/plar eklenerek veri analizi yapılabilir.

---

## Ekranlar ve Özellikler

### 1. Ana Ekran
- **Üye Ol**: Yeni bir kullanıcı kaydı oluşturmanızı sağlar.
- **Giriş Yap**: Mevcut hesabınızla giriş yapmanızı sağlar.

### 2. Bireysel Kullanıcı Ekranı
- **Takımlarım**: Kullanıcının üyesi olduğu takımları listeler ve içindeki üyeleri görüntüleme olanağı sunar.
- **Takım Oluştur**: Yeni bir takım oluşturur ve seçilen kullanıcılara takım daveti gönderir.
- **Kullanıcı Adı Değiştir**: Mevcut kullanıcı adını günceller (benzersiz olması zorunluluğu devam eder).
- **Parola Değiştirme İsteği Gönder**: Parolasını değiştirmek isteyen kullanıcılar buradan yöneticiye talep gönderir.
- **Bildirimleri Göster**: Diğer kullanıcılar veya yönetici tarafından gönderilen davet, onay veya ret mesajlarını listeler.
- **Dosya Yükle**: Lokal bir dosyayı seçerek sisteme ekler.
- **Dosya Paylaş**: Mevcut dosyayı takım üyeleriyle paylaşır.
- **Dosyalarımı Gör**: Kullanıcının sahip olduğu veya erişim izni olan dosyaları listeler.
- **Şifre Değiştir**: Yalnızca yönetici onayından sonra aktifleşen şifre değiştirme alanı.
- **Çıkış**: Oturumu sonlandırır, ana ekrana döner.

### 3. Sistem Yöneticisi Ekranı
- **Kullanıcı Profillerini Yönet**: (Örnek taslak) Tüm kullanıcıları görüntüleme, rollerini ve bilgilerini düzenleme.
- **Depolama Limitlerini Kontrol Et**: (Örnek taslak) Kullanıcıların dosya yükleme kotalarını belirleme.
- **Bildirimleri Göster**: Kullanıcılardan gelen parola değiştirme taleplerini onaylama veya reddetme.
- **Çıkış**: Oturumu sonlandırır, ana ekrana döner.

---

---
