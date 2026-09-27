# E-İmza & Mali Mühür PIN Bloke Asistanı 🔓🔏

[![Python CI](https://github.com/eimza-kep/eimza-pin-bloke-asistani/actions/workflows/ci.yml/badge.svg)](https://github.com/eimza-kep/eimza-pin-bloke-asistani/actions)
[![Lisans: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform: Cross-Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue.svg)](https://github.com)
[![Blog](https://img.shields.io/badge/Rehber-E--%C4%B0mza%20Rehberi-22c55e.svg)](https://eimza-rehberi.pages.dev/)

E-İmza ve Mali Mühür PIN kodunu 3 kez yanlış girerek bloke edenler için; yetkili sertifika sağlayıcılarından (TÜBİTAK Kamu SM, TÜRKTRUST, E-Güven, E-Tuğra, EDM Bilişim, Turkcell Mobil İmza) **PUK kodu temin adımlarını gösteren**, yeni PIN güvenlik kurallarını denetleyen ve rastgele güvenli PIN üreten açık kaynaklı yardımcı araç.

---

## ✨ Öne Çıkan Özellikler

* 🏢 **Tüm Sağlayıcılar:** Kamu SM, TÜRKTRUST, E-Güven, E-Tuğra, EDM Bilişim ve Mobil İmza kılavuzları.
* 🛡️ **Güvenli PIN Doğrulama:** Ardışık (123456), tekrarlayan (111111) ve zayıf PIN'leri engelleyen denetim motoru.
* 🎲 **Kriptografik PIN Üretici:** `--generate-pin` ile kurallara tam uyumlu rastgele 6 haneli yeni PIN üretimi.
* 🖥️ **PowerShell ve Bash Entegrasyonu:** Windows ve Linux terminal desteği.

---

## 🚀 Hızlı Başlangıç

### 1. PUK Rehberini Görüntüleme
```bash
# Tüm sağlayıcıları listeleme
python pin_assistant.py

# Sadece Kamu SM (Mali Mühür) için adımları alma
python pin_assistant.py --provider kamusm
```

### 2. Yeni Belirlenecek PIN'i Doğrulama
```bash
python pin_assistant.py --validate-pin 482915
```

### 3. Otomatik Güvenli PIN Üretme
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
* 📄 [E-İmza PIN Kodu Bloke Oldu Ne Yapmalıyım? PUK ile Kilit Çözme](https://eimza-rehberi.pages.dev/yazilar/eimza-pin-bloke-puk-kodu-sifirlama.html)
* 📄 [Mali Mühür Bloke Olduğunda PUK Kodu ile Kilit Nasıl Açılır?](https://mali-muhur-merkezi.pages.dev/yazilar/mali-muhur-pin-bloke-puk-kodu-cozum.html)
* 📄 [AKİS Akıllı Kart İzleme Aracında PIN Kilidi Açma Adımları](https://eimza-rehberi.pages.dev/yazilar/akis-kart-izleme-araci-kullanim-rehberi.html)

---

## ⚖️ Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
