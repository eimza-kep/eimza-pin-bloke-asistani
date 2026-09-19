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
param(
    [ValidateSet("KamuSM", "Turktrust", "EGuven", "ETugra", "All")]
    [string]$Provider = "All",
    [switch]$OpenPortal = $false,
    [switch]$Launch = $false,
    [switch]$NonInteractive = $false
)

try {
    $OutputEncoding = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
} catch {}

Write-Host "==========================================================================================" -ForegroundColor Cyan
Write-Host "            E-İMZA PIN BLOKE KALDIRMA VE PUK KODU ASİSTANI v1.1                           " -ForegroundColor Yellow
Write-Host "==========================================================================================`n" -ForegroundColor Cyan

Write-Host "⚠️  ÖNEMLİ UYARI:" -ForegroundColor Red
Write-Host "PIN kodunuzu 3 kez yanlış girdiğinizde e-imzanız 'BLOKE' olur." -ForegroundColor White
Write-Host "Kilidi açmak için üreticinizden alacağınız 'PUK Kodu' gereklidir." -ForegroundColor White
Write-Host "DİKKAT: PUK kodunu da 3 kez yanlış girerseniz kart kalıcı kilitlenir (yanar) ve yenisi gerekir!`n" -ForegroundColor Red

# 1. Yüklü Kart Yönetim Araçları Taraması (AKİS & SafeNet)
Write-Host "[1/3] Kart Yönetim Araçları Taranıyor..." -ForegroundColor White

$toolCandidates = @(
    @{ Name = "AKİS Kart İzleme Aracı"; Path = "$env:ProgramFiles\AKIS\akisgui.exe" },
    @{ Name = "AKİS Kart İzleme Aracı (x86)"; Path = "${env:ProgramFiles(x86)}\AKIS\akisgui.exe" },
    @{ Name = "AKİS BİLGEM"; Path = "$env:ProgramFiles\TÜBİTAK BİLGEM\AKIS\akisgui.exe" },
    @{ Name = "SafeNet Authentication Client"; Path = "$env:ProgramFiles\SafeNet\Authentication\SAC\x64\SACMonitor.exe" },
    @{ Name = "SafeNet Tools"; Path = "${env:ProgramFiles(x86)}\SafeNet\Authentication\SAC\SACMonitor.exe" }
)

$detectedTool = $null
foreach ($tool in $toolCandidates) {
    if (Test-Path $tool.Path) {
        $detectedTool = $tool
        Write-Host "  [OK] $($tool.Name) sisteminizde tespit edildi: $($tool.Path)" -ForegroundColor Green
        break
    }
}

if (-not $detectedTool) {
    Write-Host "  [!] Sistemde AKİS veya SafeNet yönetim aracı bulunamadı." -ForegroundColor Yellow
    Write-Host "      TÜBİTAK AKİS İndirme: https://akiskart.bilgem.tubitak.gov.tr/destek/" -ForegroundColor Cyan
}

# 2. Üreticiye Göre PUK Kodu Alma Portalları
$portalUrls = @{
    KamuSM    = "https://nesislemleri.kamusm.gov.tr/"
    Turktrust = "https://online.turktrust.com.tr/"
    EGuven    = "https://www.e-guven.com/"
    ETugra    = "https://www.e-tugra.com.tr/"
}

Write-Host "`n[2/3] Sertifika Sağlayıcısına Göre PUK Kodu Alma Rehberi" -ForegroundColor White
Write-Host "------------------------------------------------------------------------------------------" -ForegroundColor Gray

if ($Provider -eq "All" -or $Provider -eq "KamuSM") {
    Write-Host "1. TÜBİTAK Kamu SM (Mali Mühür & Kamu E-İmzası):" -ForegroundColor Cyan
    Write-Host "   👉 Portal: $($portalUrls.KamuSM)" -ForegroundColor White
    Write-Host "   Adımlar: 'Kilit Çözme' sekmesi > T.C. Kimlik No & Güvenlik Sözcüğü > SMS Kodu > PUK Alımı`n" -ForegroundColor Gray
}

if ($Provider -eq "All" -or $Provider -eq "Turktrust") {
    Write-Host "2. TÜRKTRUST E-İmza:" -ForegroundColor Cyan
    Write-Host "   👉 Portal: $($portalUrls.Turktrust)" -ForegroundColor White
    Write-Host "   Adımlar: Online İşlemler girişi veya 0850 222 88 75 nolu çağrı merkezinden PUK sıfırlama`n" -ForegroundColor Gray
}

if ($Provider -eq "All" -or $Provider -eq "EGuven") {
    Write-Host "3. E-Güven:" -ForegroundColor Cyan
    Write-Host "   👉 Portal: $($portalUrls.EGuven)" -ForegroundColor White
    Write-Host "   Adımlar: Online İşlemler veya 0850 222 48 83 nolu destek hattından PUK sorgulama`n" -ForegroundColor Gray
}

if ($Provider -eq "All" -or $Provider -eq "ETugra") {
    Write-Host "4. E-Tuğra:" -ForegroundColor Cyan
    Write-Host "   👉 Portal: $($portalUrls.ETugra)" -ForegroundColor White
    Write-Host "   Adımlar: Müşteri Girişi yaparak PUK sorgulama menüsünden temin edebilirsiniz`n" -ForegroundColor Gray
}

if ($OpenPortal) {
    $targetUrl = if ($Provider -ne "All" -and $portalUrls.ContainsKey($Provider)) { $portalUrls[$Provider] } else { $portalUrls.KamuSM }
    Write-Host "[*] PUK Portal bağlantısı varsayılan tarayıcıda açılıyor: $targetUrl" -ForegroundColor Green
    Start-Process $targetUrl
}

# 3. Adım Adım Kilit Çözme
Write-Host "[3/3] PUK Kodunu Aldıktan Sonra Kilit Nasıl Çözülür?" -ForegroundColor White
Write-Host "------------------------------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Kart Yönetim Aracını (AKİS veya SafeNet) açın." -ForegroundColor White
Write-Host "2. Sol taraftaki menüden sertifikanızı/kartınızı seçin." -ForegroundColor White
Write-Host "3. 'PIN İşlemleri' > 'Kilit Çöz' veya 'Unblock PIN' seçeneğine tıklayın." -ForegroundColor White
Write-Host "4. Temin ettiğiniz PUK Kodunu girin, ardından yeni 6 haneli PIN kodunuzu belirleyin." -ForegroundColor Green

if ($detectedTool) {
    if ($Launch) {
        Write-Host "`n[*] $($detectedTool.Name) başlatılıyor..." -ForegroundColor Green
        Start-Process $detectedTool.Path
    } elseif (-not $NonInteractive) {
        Write-Host "`n>>> $($detectedTool.Name) uygulamasını hemen başlatmak ister misiniz? (E/H): " -NoNewline -ForegroundColor Yellow
        $cevap = Read-Host
        if ($cevap -eq "E" -or $cevap -eq "e") {
            Start-Process $detectedTool.Path
        }
    }
}

Write-Host "`n==========================================================================================" -ForegroundColor Cyan
Write-Host " Detaylı Kılavuz: https://eimza-rehberi.pages.dev/yazilar/e-imza-pin-kodu-bloke-oldu-cozum.html " -ForegroundColor White
Write-Host "==========================================================================================`n" -ForegroundColor Cyan
