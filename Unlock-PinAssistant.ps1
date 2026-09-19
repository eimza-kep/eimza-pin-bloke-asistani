<#
.SYNOPSIS
    E-İmza PIN Bloke Kaldırma ve PUK Kod Asistanı

.DESCRIPTION
    Bu betik, e-imza PIN kodunu 3 kez hatalı girerek bloke eden kullanıcılara;
    cihazlarındaki AKİS / Kamu SM / SafeNet yazılımlarını tespit ederek
    PUK kodu temini ve PIN kilidini çözme adımlarında rehberlik eder.

.NOTES
    Yazar: E-İmza & Dijital Dönüşüm Portalı (https://eimza-rehberi.pages.dev/yazilar/e-imza-pin-kodu-bloke-oldu-cozum.html)
    Lisans: MIT
#>

[CmdletBinding()]
param()

$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "==========================================================================================" -ForegroundColor Cyan
Write-Host "            E-İMZA PIN BLOKE KALDIRMA VE PUK KODU REHBERİ v1.0                            " -ForegroundColor Yellow
Write-Host "==========================================================================================`n" -ForegroundColor Cyan

Write-Host "⚠️  ÖNEMLİ UYARI:" -ForegroundColor Red
Write-Host "PIN kodunuzu 3 kez yanlış girdiğinizde e-imzanız 'BLOKE' olur." -ForegroundColor White
Write-Host "Kilidi açmak için üreticinizden alacağınız 'PUK Kodu' gereklidir." -ForegroundColor White
Write-Host "DİKKAT: PUK kodunu da 3 kez yanlış girerseniz kart tamamen yanar (çöp olur) ve yeni e-imza almak gerekir!`n" -ForegroundColor Red

# 1. AKİS Kart İzleme Aracı Taraması
Write-Host "[1/3] AKİS Kart İzleme Aracı Aranıyor..." -ForegroundColor White

$akisPaths = @(
    "$env:ProgramFiles\AKIS\akisgui.exe",
    "${env:ProgramFiles(x86)}\AKIS\akisgui.exe",
    "$env:ProgramFiles\TÜBİTAK BİLGEM\AKIS\akisgui.exe"
)

$foundAkis = $null
foreach ($p in $akisPaths) {
    if (Test-Path $p) {
        $foundAkis = $p
        break
    }
}

if ($foundAkis) {
    Write-Host "  [OK] AKİS Kart İzleme Aracı sisteminizde kurulu: $foundAkis" -ForegroundColor Green
} else {
    Write-Host "  [!] AKİS Kart İzleme Aracı kurulu değil." -ForegroundColor Yellow
    Write-Host "      Resmi İndirme Linki: https://akiskart.bilgem.tubitak.gov.tr/destek/" -ForegroundColor Cyan
}

# 2. Üreticiye Göre PUK Kodu Alma Rehberi
Write-Host "`n[2/3] Sertifika Sağlayıcınıza Göre PUK Kodu Nasıl Alınır?" -ForegroundColor White
Write-Host "------------------------------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "1. TÜBİTAK Kamu SM (Mali Mühür & Kamu E-İmzası):" -ForegroundColor Cyan
Write-Host "   👉 https://nesislemleri.kamusm.gov.tr/ adresine gidin." -ForegroundColor White
Write-Host "   👉 'Kilit Çözme' sekmesine tıklayın." -ForegroundColor White
Write-Host "   👉 T.C. Kimlik No ve Güvenlik Sözcüğü ile SMS onayını geçerek PUK kodunuzu ekranda görün.`n" -ForegroundColor Gray

Write-Host "2. TÜRKTRUST E-İmza:" -ForegroundColor Cyan
Write-Host "   👉 https://online.turktrust.com.tr/ adresine giriş yapın veya 0850 222 88 75 nolu çağrı merkezini arayın.`n" -ForegroundColor Gray

Write-Host "3. E-Güven:" -ForegroundColor Cyan
Write-Host "   👉 https://www.e-guven.com/ 'Online İşlemler' veya 0850 222 48 83 nolu destek hattını arayın.`n" -ForegroundColor Gray

Write-Host "4. E-Tuğra:" -ForegroundColor Cyan
Write-Host "   👉 https://www.e-tugra.com.tr/ adresinden Müşteri Girişi yaparak PUK sorgulayın.`n" -ForegroundColor Gray

# 3. Adım Adım Kilit Çözme
Write-Host "[3/3] PUK Kodunu Aldıktan Sonra Kilit Nasıl Çözülür?" -ForegroundColor White
Write-Host "------------------------------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "1. AKİS Kart İzleme Aracını açın." -ForegroundColor White
Write-Host "2. Sol taraftaki menüden sertifikanızı seçin." -ForegroundColor White
Write-Host "3. Üstteki menüden 'PIN İşlemleri' > 'Kilit Çöz' butonuna tıklayın." -ForegroundColor White
Write-Host "4. Aldığınız PUK Kodunu girin, ardından KENDİ BELİRLEYECEĞİNİZ yeni bir 6 haneli PIN yazıp onaylayın." -ForegroundColor Green

if ($foundAkis) {
    Write-Host "`n>>> AKİS Kart İzleme Aracını hemen başlatmak ister misiniz? (E/H): " -NoNewline -ForegroundColor Yellow
    $cevap = Read-Host
    if ($cevap -eq "E" -or $cevap -eq "e") {
        Start-Process $foundAkis
    }
}

Write-Host "`n==========================================================================================" -ForegroundColor Cyan
Write-Host " Detaylı Kılavuz: https://eimza-rehberi.pages.dev/yazilar/e-imza-pin-kodu-bloke-oldu-cozum.html                                 " -ForegroundColor White
Write-Host "==========================================================================================`n" -ForegroundColor Cyan
