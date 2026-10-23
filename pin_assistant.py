#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-İmza PIN Bloke Kaldırma, PUK Kodu & Güvenli PIN Üretici Asistanı v1.3
======================================================================
Türkiye'deki tüm yetkili ESHS ve GSM operatörlerinin (Kamu SM, TÜRKTRUST,
E-Güven, E-Tuğra, EDM, Turkcell, Vodafone, TT) PUK temin adımlarını, güvenli
PIN kurallarını, PUK doğrulamayı, APDU sıfırlama komutlarını ve görsel rehberleri sağlar.

Özellikler:
- Sıfır Harici Bağımlılık (Pure Python Standart Kütüphane)
- e-Devlet ile Kamu SM PUK temin adımları ve görsel rehber
- AKİS ve CardOS ISO 7816-4 RESET RETRY COUNTER (0x2C) APDU üreteci
- Güvenli PIN (6-8 basamak) kural denetimi ve rastgele PIN üretimi
- PUK format doğrulaması (validate_puk)
- Çevrimdışı HTML Görsel Rehber üretimi (--html-guide)
- İnteraktif terminal asistanı (--wizard)

Yazar: E-İmza & Dijital Dönüşüm Portalı (https://eimzabilgi.site/)
Lisans: MIT
"""

import sys
import os
import re
import secrets
import json

# Windows konsolunda UTF-8 çıktı desteği
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROVIDERS = {
    "kamusm": {
        "name": "TÜBİTAK Kamu SM",
        "description": "Kamu çalışanları ve resmi kurum mali mühür / e-imza kartları",
        "portal_url": "https://kisisel.kamusm.gov.tr/",
        "puk_guide": "1. Kamu SM Online İşlemler sayfasına (kisisel.kamusm.gov.tr) e-Devlet veya SMS şifrenizle giriş yapın.\n2. Sol menüden 'PIN / PUK İşlemleri' seçeneğine tıklayın.\n3. Kartınız için oluşturulmuş 8 haneli PUK kodunu ekrandan not alın.\n4. Bilgisayarınızda 'AKİS Kart İzleme Aracı'nı açıp 'PIN Kilidi Aç' butonuna basarak PUK kodu ve yeni PIN'inizi girin."
    },
    "turktrust": {
        "name": "TÜRKTRUST",
        "description": "Bireysel ve kurumsal nitelikli elektronik sertifikalar",
        "portal_url": "https://online.turktrust.com.tr/",
        "puk_guide": "1. TÜRKTRUST Online İşlemler sayfasına giriş yapın.\n2. Kart İşlemleri > PUK Kodu Sorgulama adımını takip edin.\n3. SAC (SafeNet) veya Palma yazılımından PUK kodu ile PIN kilidini kaldırın."
    },
    "eguven": {
        "name": "E-Güven",
        "description": "Bireysel ve kurumsal e-imza çözümleri",
        "portal_url": "https://e-imza.e-guven.com/",
        "puk_guide": "1. E-Güven Online İşlemler merkezine girin.\n2. Telefonunuza gelen SMS onay kodu ile PUK kodunuzu sorgulayın.\n3. SafeNet SAC yazılımında 'Set Smart Card PIN' adımından yeni PIN oluşturun."
    },
    "etugra": {
        "name": "E-Tuğra (EBG)",
        "description": "Nitelikli elektronik sertifika hizmet sağlayıcısı",
        "portal_url": "https://www.e-tugra.com.tr/",
        "puk_guide": "1. E-Tuğra Kullanıcı Portalı'ndan TC Kimlik ve SMS onayı ile giriş yapın.\n2. Sertifika Yönetimi > PUK Kodunu Göster seçeneğine tıklayın.\n3. AKİS veya CardOS yönetim panelinden PIN kilidini çözün."
    },
    "edmbilisim": {
        "name": "EDM Bilişim",
        "description": "EDM e-imza ve KEP kurumsal çözümleri",
        "portal_url": "https://portal.edmbilisim.com.tr/",
        "puk_guide": "1. EDM Müşteri Portalı'na giriş yapın.\n2. E-İmza İşlemleri sekmesinden PUK Kodu Al düğmesine basın.\n3. USB Token yönetim panelinde PUK girerek yeni PIN belirleyin."
    },
    "eimzatr": {
        "name": "E-İmzaTR",
        "description": "Nitelikli elektronik sertifika ve USB token çözümleri",
        "portal_url": "https://www.e-imzatr.com.tr/",
        "puk_guide": "1. E-İmzaTR Müşteri Portalı'na kimlik bilgilerinizle giriş yapın.\n2. Sertifika Yönetimi > PUK Kodu Öğrenme adımlarını izleyin.\n3. AKİS yönetim aracında PUK girerek yeni PIN belirleyin."
    },
    "turkcell": {
        "name": "Turkcell Mobil İmza",
        "description": "SIM kart tabanlı mobil elektronik imza",
        "portal_url": "https://www.turkcell.com.tr/",
        "puk_guide": "1. 3 kez yanlış girilen Mobil İmza şifresi bloke olur.\n2. Turkcell Müşteri Hizmetleri (532) veya Turkcell Mağazaları üzerinden kimlik doğrulamasıyla yeni şifre oluşturulmalıdır."
    },
    "vodafone": {
        "name": "Vodafone Mobil İmza",
        "description": "Vodafone SIM kart tabanlı mobil elektronik imza servisi",
        "portal_url": "https://www.vodafone.com.tr/",
        "puk_guide": "1. Bloke olan mobil imzanız için 542 Müşteri Hizmetleri aranmalıdır.\n2. Güvenlik teyidinin ardından mobil imza şifre sıfırlama talebi oluşturulur."
    },
    "turktelekom": {
        "name": "Türk Telekom Mobil İmza",
        "description": "Türk Telekom SIM kart tabanlı mobil imza servisi",
        "portal_url": "https://www.turktelekom.com.tr/",
        "puk_guide": "1. 3 hatalı şifre denemesi sonrası mobil imza bloke olur.\n2. 444 1 444 Müşteri Hizmetleri veya Türk Telekom Ofislerinden şifre yenileme yapılır."
    }
}

def validate_pin(pin: str) -> dict:
    """
    Yeni oluşturulacak E-İmza PIN'inin güvenlik kurallarını denetler:
    - 6 ila 8 hane arasında olmalı (genelde sadece rakam)
    - Tamamı aynı rakamlardan oluşamaz (111111 vb.)
    - Ardışık rakam dizisi olamaz (123456, 654321 vb.)
    """
    if not isinstance(pin, str):
        pin = str(pin)

    pin = pin.strip()

    if not pin.isdigit():
        return {"valid": False, "reason": "PIN yalnızca rakamlardan oluşmalıdır."}

    if len(pin) < 6 or len(pin) > 8:
        return {"valid": False, "reason": f"PIN uzunluğu 6-8 basamak olmalıdır. (Girilen: {len(pin)})"}

    if len(set(pin)) == 1:
        return {"valid": False, "reason": "PIN tüm basamakları aynı olan rakamlardan oluşamaz (ör. 111111)."}

    # Ardışık artan veya azalan kontrolü
    is_sequential_inc = all(int(pin[i+1]) - int(pin[i]) == 1 for i in range(len(pin)-1))
    is_sequential_dec = all(int(pin[i]) - int(pin[i+1]) == 1 for i in range(len(pin)-1))

    if is_sequential_inc:
        return {"valid": False, "reason": "PIN ardışık artan rakamlardan oluşamaz (ör. 123456)."}
    if is_sequential_dec:
        return {"valid": False, "reason": "PIN ardışık azalan rakamlardan oluşamaz (ör. 654321)."}

    return {"valid": True, "reason": "PIN kurallara uygun ve güvenli."}

def validate_puk(puk: str) -> dict:
    """
    Girilen PUK kodunun biçimini ve geçerlilik standartlarını denetler:
    - 8 karakter uzunluğunda olmalıdır.
    - Alfanümerik veya yalnızca rakam olmalıdır.
    - Tamamı aynı veya boş olamaz.
    """
    if not isinstance(puk, str):
        puk = str(puk)

    puk = puk.strip()

    if len(puk) != 8:
        return {"valid": False, "reason": f"PUK kodu tam 8 karakter olmalıdır. (Girilen: {len(puk)})"}

    if not re.match(r'^[A-Za-z0-9]{8}$', puk):
        return {"valid": False, "reason": "PUK kodu yalnızca harf ve rakamlardan oluşmalıdır."}

    if len(set(puk)) == 1:
        return {"valid": False, "reason": "PUK kodu geçersiz (tüm karakterler aynı olamaz)."}

    return {"valid": True, "reason": "PUK kodu standart biçime uygun."}

def generate_secure_pin(length=6) -> str:
    """Kurallara tam uyumlu kriptografik rastgele güvenli PIN üretir."""
    if length < 6:
        length = 6
    if length > 8:
        length = 8

    while True:
        digits = [str(secrets.randbelow(10)) for _ in range(length)]
        candidate = "".join(digits)
        if validate_pin(candidate)["valid"]:
            return candidate

def generate_puk_unblock_apdu(card_type: str, puk_code: str, new_pin: str) -> dict:
    """
    AKİS (TÜBİTAK) ve CardOS (Siemens/Atos) akıllı kartları için
    ISO 7816-4 RESET RETRY COUNTER (0x2C) APDU komut dizisi üretir.
    """
    card_type_norm = card_type.lower().strip()
    puk_clean = puk_code.strip()
    new_pin_clean = new_pin.strip()

    val_puk = validate_puk(puk_clean)
    if not val_puk["valid"]:
        raise ValueError(f"Geçersiz PUK: {val_puk['reason']}")

    val_pin = validate_pin(new_pin_clean)
    if not val_pin["valid"]:
        raise ValueError(f"Geçersiz yeni PIN: {val_pin['reason']}")

    puk_padded = puk_clean.ljust(8, "F")[:8]
    new_pin_padded = new_pin_clean.ljust(8, "F")[:8]

    puk_hex = " ".join(f"{ord(c):02X}" if c != "F" else "FF" for c in puk_padded)
    pin_hex = " ".join(f"{ord(c):02X}" if c != "F" else "FF" for c in new_pin_padded)

    if "cardos" in card_type_norm:
        apdu = f"00 2C 00 01 10 {puk_hex} {pin_hex}"
        explanation = "CardOS ISO 7816-4 RESET RETRY COUNTER (Unblock & Set PIN)"
    else:
        apdu = f"00 2C 02 81 10 {puk_hex} {pin_hex}"
        explanation = "TÜBİTAK AKİS / PKCS#15 Standard Reset Retry Counter APDU"

    return {
        "card_type": card_type,
        "apdu_hex": apdu,
        "explanation": explanation,
        "expected_response": "90 00 (SW1/SW2 Başarılı)",
        "terminal_command": f"echo \"{apdu.replace(' ', '')}\" | opensc-tool -s"
    }

def get_provider_info(provider_key: str):
    """Sağlayıcı anahtarı ile sağlayıcı bilgilerini döndürür."""
    return PROVIDERS.get(provider_key.lower().strip())

def generate_html_guide() -> str:
    """Tüm adımları, portalları ve SVG infografikleri içeren bağımsız HTML rehber üretir."""
    provider_cards_html = ""
    for key, p in PROVIDERS.items():
        provider_cards_html += f"""
        <div class="card">
            <h3>🏢 {p['name']}</h3>
            <p><strong>Açıklama:</strong> {p['description']}</p>
            <p><strong>Portal:</strong> <a href="{p['portal_url']}" target="_blank">{p['portal_url']}</a></p>
            <div class="steps">
                <strong>PUK Alma Adımları:</strong>
                <pre>{p['puk_guide']}</pre>
            </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-İmza PIN Bloke Kaldırma ve PUK Rehberi v1.3</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        header {{ text-align: center; margin-bottom: 40px; }}
        h1 {{ color: #38bdf8; }}
        .badge {{ background: #0284c7; color: #fff; padding: 4px 10px; border-radius: 999px; font-size: 13px; font-weight: bold; }}
        .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 20px; margin-bottom: 20px; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        pre {{ background: #0f172a; padding: 12px; border-radius: 8px; color: #cbd5e1; font-family: monospace; white-space: pre-wrap; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; }}
        .alert-box {{ background: #450a0a; border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; margin: 20px 0; }}
        .info-box {{ background: #082f49; border-left: 4px solid #0284c7; padding: 15px; border-radius: 6px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔓 E-İmza PIN Bloke Kaldırma & PUK Rehberi <span class="badge">v1.3</span></h1>
            <p>Türkiye'deki tüm ESHS ve GSM operatörleri için adım adım PIN kurtarma rehberi.</p>
        </header>

        <div class="alert-box">
            <strong>⚠️ Önemli Güvenlik Uyarısı:</strong> E-İmza PIN kodu 3 kez yanlış girildiğinde kart bloke olur ve PUK kodu gerekir. 
            <strong>PUK kodunun da 3 kez hatalı girilmesi durumunda kart kalıcı olarak kilitlenir (yanar)</strong> ve yeni kart başvurusu yapılması zorunlu hale gelir.
        </div>

        <div class="info-box">
            <strong>💡 TÜBİTAK Kamu SM e-Devlet Girişi:</strong> Kamu çalışanları ve Mali Mühür sahipleri <a href="https://kisisel.kamusm.gov.tr/" target="_blank">kisisel.kamusm.gov.tr</a> adresine doğrudan <strong>e-Devlet ile Giriş</strong> yaparak anında PUK kodlarını öğrenebilirler.
        </div>

        <h2>🏢 ESHS ve GSM Operatörleri</h2>
        <div class="grid">
            {provider_cards_html}
        </div>

        <footer style="text-align: center; margin-top: 50px; color: #64748b; font-size: 13px;">
            Açık Kaynak Proje: <a href="https://github.com/eimza-kep/eimza-pin-bloke-asistani" target="_blank">eimza-pin-bloke-asistani</a> | MIT Lisansı
        </footer>
    </div>
</body>
</html>"""
    return html

def run_interactive_wizard():
    """Kullanıcıyı adım adım yönlendiren terminal asistanı."""
    print("\n" + "=" * 70)
    print("      E-İMZA PIN BLOKE KALDIRMA İNTERAKTİF ASİSTANI v1.3")
    print("=" * 70)

    print("\nLütfen E-İmza / Mali Mühür sağlayıcınızı seçin:")
    prov_keys = list(PROVIDERS.keys())
    for idx, k in enumerate(prov_keys, 1):
        print(f"  [{idx}] {PROVIDERS[k]['name']}")

    try:
        choice = input("\nSeçiminiz (1-9): ").strip()
        idx = int(choice) - 1
        if idx < 0 or idx >= len(prov_keys):
            print("Geçersiz seçim.")
            return
        selected_key = prov_keys[idx]
        provider = PROVIDERS[selected_key]
    except Exception:
        print("Geçersiz giriş.")
        return

    print(f"\nSeçilen Sağlayıcı: {provider['name']}")
    print(f"Online İşlemler Portalı: {provider['portal_url']}")
    print("\nAdım 1: Portal üzerinden PUK kodunuzu alın:")
    for line in provider["puk_guide"].split("\n"):
        print(f"  {line}")

    print("\n" + "-" * 70)
    puk_input = input("Portaldan aldığınız 8 haneli PUK kodunu girin (Test için Enter): ").strip()
    if puk_input:
        val_puk = validate_puk(puk_input)
        if not val_puk["valid"]:
            print(f"[!] HATA: {val_puk['reason']}")
            return
        print(f"[✓] {val_puk['reason']}")
    else:
        puk_input = "12345678"
        print(f"Örnek PUK kullanılıyor: {puk_input}")

    print("\nAdım 2: Yeni bir 6 haneli güvenli PIN belirleyin.")
    gen_choice = input("Otomatik güvenli rastgele PIN üretilsin mi? (E/h): ").strip().lower()
    if gen_choice in ["", "e", "evet", "y"]:
        new_pin = generate_secure_pin(6)
        print(f"🔒 Üretilen Güvenli PIN: {new_pin}")
    else:
        new_pin = input("Yeni PIN kodunuzu girin (6 basamak): ").strip()
        val_pin = validate_pin(new_pin)
        if not val_pin["valid"]:
            print(f"[!] HATA: {val_pin['reason']}")
            return
        print(f"[✓] {val_pin['reason']}")

    print("\nAdım 3: AKİS veya APDU ile Kilidi Çözün:")
    try:
        apdu = generate_puk_unblock_apdu("akis", puk_input, new_pin)
        print(f"APDU Komutu : {apdu['apdu_hex']}")
        print(f"Terminal    : {apdu['terminal_command']}")
    except Exception as e:
        print(f"APDU oluşturulamadı: {e}")

    print("\n[✓] Tebrikler! AKİS Kart İzleme Aracı üzerinden 'PIN Kilidi Aç' diyerek yeni PIN'inizi kullanmaya başlayabilirsiniz.")
    print("=" * 70 + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="E-İmza PIN Bloke Kaldırma, PUK ve Güvenli PIN Asistanı v1.3")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()) + ["all"], default="all", help="E-imza sağlayıcısı")
    parser.add_argument("--validate-pin", help="Yeni belirlenecek PIN kodunun güvenliğini test et")
    parser.add_argument("--validate-puk", help="Girilen 8 haneli PUK kodunun formatını denetler")
    parser.add_argument("--generate-pin", action="store_true", help="Güvenli, kurallara uygun rastgele 6 haneli yeni PIN üretir")
    parser.add_argument("--generate-apdu", action="store_true", help="AKİS / CardOS kartlar için PUK ile PIN sıfırlama APDU komut dizisi üretir")
    parser.add_argument("--card-type", choices=["akis", "cardos"], default="akis", help="Akıllı kart donanım tipi (akis veya cardos)")
    parser.add_argument("--puk", help="Sıfırlama için girilecek PUK kodu")
    parser.add_argument("--new-pin", help="Yeni belirlenecek 6 haneli PIN")
    parser.add_argument("--wizard", "--interactive", dest="wizard", action="store_true", help="Adım adım yönlendiren interaktif asistanı başlatır")
    parser.add_argument("--html-guide", help="Çevrimdışı görsel HTML rehberini belirtilen dosyaya kaydeder")
    parser.add_argument("--json", action="store_true", help="JSON formatında çıktı üretir")

    args = parser.parse_args()

    if args.wizard:
        run_interactive_wizard()
        return

    if args.html_guide:
        html = generate_html_guide()
        with open(args.html_guide, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[✓] Çevrimdışı HTML rehberi '{args.html_guide}' dosyasına başarıyla kaydedildi.")
        return

    if args.validate_puk:
        res = validate_puk(args.validate_puk)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            if res["valid"]:
                print(f"[✓] Başarılı: {res['reason']}")
            else:
                print(f"[!] HATA: {res['reason']}")
                sys.exit(1)
        return

    if args.generate_apdu:
        puk = args.puk or "12345678"
        new_pin = args.new_pin or "482915"
        try:
            res_apdu = generate_puk_unblock_apdu(args.card_type, puk, new_pin)
            if args.json:
                print(json.dumps(res_apdu, indent=2, ensure_ascii=False))
            else:
                print("=" * 65)
                print(f"APDU PUK BLOKE ÇÖZME KOMUT DİZİSİ ({res_apdu['card_type'].upper()})")
                print("=" * 65)
                print(f"Komut Hex         : {res_apdu['apdu_hex']}")
                print(f"Açıklama          : {res_apdu['explanation']}")
                print(f"Beklenen Yanıt    : {res_apdu['expected_response']}")
                print(f"Terminal Çalıştırma: {res_apdu['terminal_command']}")
                print("=" * 65)
        except Exception as e:
            print(f"[!] HATA: {e}", file=sys.stderr)
            sys.exit(1)
        return

    if args.generate_pin:
        pin = generate_secure_pin(6)
        if args.json:
            print(json.dumps({"generated_pin": pin, "length": 6, "status": "SECURE"}, indent=2))
        else:
            print(f"🔒 Üretilen Güvenli PIN: {pin} (6 Basamaklı)")
            print("💡 AKİS veya SafeNet yönetim yazılımında bu kodu yeni PIN olarak belirleyebilirsiniz.")
        return

    if args.validate_pin:
        res = validate_pin(args.validate_pin)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            if res["valid"]:
                print(f"[✓] Başarılı: {res['reason']}")
            else:
                print(f"[!] HATA: {res['reason']}")
                sys.exit(1)
        return

    if args.json:
        selected = PROVIDERS if args.provider == "all" else {args.provider: PROVIDERS[args.provider]}
        print(json.dumps(selected, indent=2, ensure_ascii=False))
        return

    print("=" * 65)
    print("      E-İMZA PIN BLOKE KALDIRMA VE PUK REHBERİ v1.3")
    print("=" * 65)

    selected = PROVIDERS.keys() if args.provider == "all" else [args.provider]

    for key in selected:
        p = PROVIDERS[key]
        print(f"\n🏢 {p['name']}")
        print(f"   Açıklama   : {p['description']}")
        print(f"   PUK Portalı: {p['portal_url']}")
        print("   Adımlar    :")
        for line in p["puk_guide"].split("\n"):
            print(f"     {line}")

    print("\n" + "=" * 65)
    print("💡 İPUCU: Güvenli rastgele yeni PIN üretmek için: python pin_assistant.py --generate-pin")
    print("💡 İPUCU: İnteraktif asistanı başlatmak için    : python pin_assistant.py --wizard")

if __name__ == "__main__":
    main()
