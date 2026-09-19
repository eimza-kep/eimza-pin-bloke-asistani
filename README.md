# E-İmza PIN Bloke Kaldırma ve PUK Asistanı 🔒🆘

[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue.svg)](https://microsoft.com)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1%2B%20%7C%207%2B-blueviolet.svg)](https://github.com/PowerShell/PowerShell)

E-İmza veya Mali Mühür PIN kodunu **3 kez üst üste yanlış girerek cihazı bloke eden** kullanıcılar için adım adım PUK kodu alma ve AKİS üzerinden kilidi açma rehberi ve asistanıdır.

---

## ⚠️ Kritik Güvenlik Kuralı

* E-imza çipinin donanımsal güvenlik mimarisi gereği PIN kodu 3 kez yanlış girildiğinde cihaz kendini kilitler (**BLOKE**).
* Kilidi açmak için **PUK Kodu** şarttır.
* **DİKKAT:** PUK kodunu da 3 kez hatalı girerseniz akıllı kart kalıcı olarak kilitlenir (**Kart Yanar**) ve ücreti karşılığında sıfırdan yeni e-imza üretilmesi gerekir! Bu nedenle rastgele PUK denemesi yapmayınız!

---

## 🚀 Hızlı Kullanım

1. Repoyu indirin ve **`pin-kurtarma.bat`** dosyasına çift tıklayın.
2. Sisteminizdeki AKİS Kart İzleme Aracı taranacak ve doğrudan kilit çözme ekranı başlatılacaktır.

---

## 🏢 Sağlayıcılara Göre PUK Kodu Nasıl Alınır?

### 1. TÜBİTAK Kamu SM (Mali Mühür & Kamu E-İmzası)
* [Kamu SM NES İşlemleri](https://nesislemleri.kamusm.gov.tr/) sayfasına gidin.
* **"Kilit Çözme"** menüsünü seçin.
* T.C. Kimlik No ve e-imza başvurusunda belirlediğiniz Güvenlik Sözcüğü ile giriş yapın.
* Telefonunuza gelen SMS onay kodunu girerek PUK kodunuzu ekrandan öğrenin.

### 2. TÜRKTRUST
* [TÜRKTRUST Online İşlemler](https://online.turktrust.com.tr/) portalına girin veya `0850 222 88 75` nolu destek hattını arayarak PUK sıfırlama talep edin.

### 3. E-Güven
* [E-Güven Online İşlem Merkezi](https://www.e-guven.com/) veya `0850 222 48 83` nolu çağrı merkezinden PUK temin edebilirsiniz.

### 4. E-Tuğra
* [E-Tuğra Müşteri Portalı](https://www.e-tugra.com.tr/) üzerinden kimlik doğrulama ile PUK sorgulanabilir.

---

## 🛠️ PUK Kodunu Aldıktan Sonra AKİS ile Kilit Çözme

1. **AKİS Kart İzleme Aracını** açın (Başlat menüsünden aratabilirsiniz).
2. Sol tarafta e-imzanızı ve adınızı seçin.
3. Üst menüden **"PIN İşlemleri" > "Kilit Çöz"** butonuna basın.
4. Sağlayıcınızdan aldığınız **PUK Kodunu** girin.
5. Alt kutucuklara unutmayacağınız yeni bir **6 haneli PIN** yazıp onaylayın.
6. Kartınızın kilidi anında açılacaktır!

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) kapsamında sunulmaktadır.
