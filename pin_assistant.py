#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E-İmza PIN Bloke Kaldırma ve PUK Kodu Asistanı
Sağlayıcı bazlı PUK temin portalları ve güvenli yeni PIN doğrulama motoru.
"""

import sys
import re

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

def get_provider_info(provider_key: str):
    return PROVIDERS.get(provider_key.lower().strip())

def main():
    import argparse
    parser = argparse.ArgumentParser(description="E-İmza PIN Bloke Kaldırma ve PUK Asistanı")
    parser.add_argument("--provider", choices=["kamusm", "turktrust", "eguven", "etugra", "all"], default="all", help="E-imza sağlayıcısı")
    parser.add_argument("--validate-pin", help="Yeni belirlenecek PIN kodunun güvenliğini test et")
    args = parser.parse_args()

    if args.validate_pin:
        res = validate_pin(args.validate_pin)
        if res["valid"]:
            print(f"[✓] Başarılı: {res['reason']}")
        else:
            print(f"[!] HATA: {res['reason']}")
            sys.exit(1)
        return

    print("=" * 65)
    print("      E-İMZA PIN BLOKE KALDIRMA VE PUK REHBERİ")
    print("=" * 65)

    selected = PROVIDERS.keys() if args.provider == "all" else [args.provider]
    for key in selected:
        info = PROVIDERS[key]
        print(f"\n🏢 {info['name']} ({info['description']})")
        print(f"🔗 Online PUK Portalı: {info['portal_url']}")
        print("📋 Çözüm Adımları:")
        for line in info['puk_guide'].split("\n"):
            print(f"   {line}")

    print("\n" + "=" * 65)
    print("⚠️ UYARI: PUK kodunu 3 defa hatalı girerseniz kartınız KULLANILAMAZ hale gelir!")
    print("=" * 65)

if __name__ == "__main__":
    main()
