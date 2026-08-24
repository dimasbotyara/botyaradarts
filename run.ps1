# run.ps1
$ErrorActionPreference = "Continue"

if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "[OK] Виртуальное окружение найдено, активирую..." -ForegroundColor Green
    & ".venv\Scripts\Activate.ps1"
    python app.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "[ERROR] Произошла ошибка при запуске." -ForegroundColor Red
        Read-Host "Нажмите Enter для выхода"
        exit 1
    }
    exit 0
} else {
    Write-Host "[INFO] Виртуальное окружение .venv не найдено." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "=== Как создать виртуальное окружение ===" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[RU]"
    Write-Host "1. Откройте терминал в папке проекта."
    Write-Host "2. Выполните:  python -m venv .venv"
    Write-Host "3. Активируйте:  .venv\Scripts\Activate.ps1"
    Write-Host "4. Установите зависимости:  pip install -r requirements.txt"
    Write-Host "5. Запустите игру:  python app.py"
    Write-Host ""
    Write-Host "[EN]"
    Write-Host "1. Open terminal in project folder."
    Write-Host "2. Run:  python -m venv .venv"
    Write-Host "3. Activate:  .venv\Scripts\Activate.ps1"
    Write-Host "4. Install dependencies:  pip install -r requirements.txt"
    Write-Host "5. Run game:  python app.py"
    Write-Host ""
    Read-Host "Нажмите Enter для выхода"
    exit 1
}
