# E-İmza PIN Bloke Kaldırma ve PUK Asistanı 🔓🔑

[![Python CI](https://github.com/eimza-kep/eimza-pin-bloke-asistani/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/eimza-pin-bloke-asistani/actions)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](https://github.com)
[![Blog](https://img.shields.io/badge/Rehber-E--%C4%B0mza%20Rehberi-22c55e.svg)](https://eimzabilgi.site/)

Türkiye'deki yetkili Elektronik Sertifika Hizmet Sağlayıcıları (Kamu SM, TÜRKTRUST, E-Güven, E-Tuğra, EDM Bilişim, E-İmzaTR) ve GSM operatörlerinin (Turkcell, Vodafone, Türk Telekom Mobil İmza) e-imza USB token PIN bloke kaldırma adımlarını, PUK sorgulama portallarını ve APDU komut dizilerini sunan açık kaynaklı asistan.

---

## ✨ Öne Çıkan Özellikler

* 🏢 **Tam ESHS ve GSM Kapsamı:** Kamu SM, TÜRKTRUST, E-Güven, E-Tuğra, EDM, E-İmzaTR ve Mobil İmza servisleri.
* ⚡ **AKİS & CardOS APDU Üreteci:** ISO 7816-4 RESET RETRY COUNTER (`0x2C`) komut dizisi ile terminalden doğrudan PUK açma.
* 🛡️ **Güvenli PIN Doğrulama:** Ardışık (123456), tekrarlayan (111111) ve zayıf PIN'leri engelleyen denetim motoru.
* 🎲 **Kriptografik PIN Üretici:** `--generate-pin` ile kurallara tam uyumlu rastgele 6 haneli yeni PIN üretimi.
* 🖥️ **PowerShell ve Bash Entegrasyonu:** Windows, Linux ve macOS terminal desteği.

---

## 🚀 Hızlı Başlangıç

### 1. PUK Rehberini Görüntüleme
```bash
# Tüm sağlayıcıları listeleme
python pin_assistant.py

# Sadece Kamu SM (Mali Mühür) için adımları alma
python pin_assistant.py --provider kamusm
```

### 2. AKİS & CardOS İçin APDU PUK Sıfırlama Komutu Üretme
```bash
# AKİS akıllı kartlar için APDU komutu
python pin_assistant.py --generate-apdu --card-type akis --puk 12345678 --new-pin 482915

# Siemens/Atos CardOS kartlar için APDU komutu
python pin_assistant.py --generate-apdu --card-type cardos --puk 12345678 --new-pin 482915
```

### 3. Yeni Belirlenecek PIN'i Doğrulama
```bash
python pin_assistant.py --validate-pin 482915
```

### 4. Otomatik Güvenli PIN Üretme
```bash
python pin_assistant.py --generate-pin
```

---

## 🔗 E-Dönüşüm Açık Kaynak Ekosistemi

Bu araç [eimza-kep](https://github.com/eimza-kep) organizasyonunun açık kaynak e-dönüşüm araçları ekosisteminin bir parçasıdır:

* 🇹🇷 **[awesome-turkiye-e-donusum](https://github.com/eimza-kep/awesome-turkiye-e-donusum):** Türkiye E-Dönüşüm kütüphane, mevzuat ve araçlar listesi.
* 🩺 **[akilli-kart-surucu-teshis](https://github.com/eimza-kep/akilli-kart-surucu-teshis):** Akıllı kart okuyucu ve sürücü teşhis aracı.
* ⏱️ **[mali-muhur-eimza-suresi-kontrol](https://github.com/eimza-kep/mali-muhur-eimza-suresi-kontrol):** Sertifika kalan gün denetimi ve bildirim scripti.
* 📄 **[python-pdf-eimza-dogrulayici](https://github.com/eimza-kep/python-pdf-eimza-dogrulayici):** PDF belgelerindeki PAdES e-imzaları doğrulama aracı.

---

## 📚 İlgili Teknik Rehberler
* 📄 [E-İmza PIN Kodu Bloke Oldu Ne Yapmalıyım? PUK ile Kilit Çözme](https://eimzabilgi.site/yazilar/eimza-pin-bloke-puk-kodu-sifirlama.html)
* 📄 [Mali Mühür Bloke Olduğunda PUK Kodu ile Kilit Nasıl Açılır?](https://malimuhur.site/yazilar/mali-muhur-pin-bloke-puk-kodu-cozum.html)
* 📄 [AKİS Akıllı Kart İzleme Aracında PIN Kilidi Açma Adımları](https://eimzabilgi.site/yazilar/akis-kart-izleme-araci-kullanim-rehberi.html)

---
