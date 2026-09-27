#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-İmza PIN Bloke Kaldırma, PUK Kodu & Güvenli PIN Üretici Asistanı v1.2
======================================================================
Türkiye'deki tüm yetkili ESHS ve GSM operatörlerinin (Kamu SM, TÜRKTRUST,
E-Güven, E-Tuğra, EDM, Turkcell, Vodafone, TT) PUK temin adımlarını, güvenli
PIN kurallarını ve kriptografik rastgele yeni PIN üretimini sağlar.

Yazar: E-İmza & Dijital Dönüşüm Portalı (https://eimza-rehberi.pages.dev/)
Lisans: MIT
"""

import sys
import re
import secrets
import json

# Force UTF-8 stdout
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
        "puk_guide": "1. Kamu SM Online İşlemler sayfasına e-Devlet veya SMS şifrenizle giriş yapın.\n2. 'PIN / PUK İşlemleri' menüsüne tıklayın.\n3. Kartınız için PUK kodunu ekrandan not alın.\n4. AKİS Kart İzleme Aracı'nı açıp 'PIN Kilidi Aç' butonuna basarak yeni PIN belirleyin."
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
    "turkcell": {
        "name": "Turkcell Mobil İmza",
        "description": "SIM kart tabanlı mobil elektronik imza",
        "portal_url": "https://www.turkcell.com.tr/",
        "puk_guide": "1. 3 kez yanlış girilen Mobil İmza şifresi bloke olur.\n2. Turkcell Müşteri Hizmetleri (532) veya Turkcell Mağazaları üzerinden kimlik doğrulamasıyla yeni şifre oluşturulmalıdır."
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

def get_provider_info(provider_key: str):
    return PROVIDERS.get(provider_key.lower().strip())

def main():
    import argparse
    parser = argparse.ArgumentParser(description="E-İmza PIN Bloke Kaldırma ve PUK Asistanı v1.2")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()) + ["all"], default="all", help="E-imza sağlayıcısı")
    parser.add_argument("--validate-pin", help="Yeni belirlenecek PIN kodunun güvenliğini test et")
    parser.add_argument("--generate-pin", action="store_true", help="Güvenli, kurallara uygun rastgele 6 haneli yeni PIN üretir")
    parser.add_argument("--json", action="store_true", help="JSON çıktısı ver")

    args = parser.parse_args()

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
    print("      E-İMZA PIN BLOKE KALDIRMA VE PUK REHBERİ v1.2")
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

if __name__ == "__main__":
    main()
