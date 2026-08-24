@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul

if exist ".venv\Scripts\activate.bat" (
    echo [OK] Виртуальное окружение найдено, активирую...
    call ".venv\Scripts\activate.bat"
    python app.py
    if errorlevel 1 (
        echo.
        echo [ERROR] Произошла ошибка при запуске.
        pause
    )
    exit /b 0
) else (
    echo [INFO] Виртуальное окружение .venv не найдено.
    echo.
    echo === Как создать виртуальное окружение ===
    echo.
    echo [RU]
    echo 1. Откройте терминал в папке проекта.
    echo 2. Выполните:  python -m venv .venv
    echo 3. Активируйте:  .venv\Scripts\activate
    echo 4. Установите зависимости:  pip install -r requirements.txt
    echo 5. Запустите игру:  python app.py
    echo.
    echo [EN]
    echo 1. Open terminal in project folder.
    echo 2. Run:  python -m venv .venv
    echo 3. Activate:  .venv\Scripts\activate
    echo 4. Install dependencies:  pip install -r requirements.txt
    echo 5. Run game:  python app.py
    echo.
    pause
    exit /b 1
)
