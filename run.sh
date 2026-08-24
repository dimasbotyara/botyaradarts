#!/bin/bash

if [ -f ".venv/bin/activate" ]; then
    echo "[OK] Виртуальное окружение найдено, активирую..."
    source .venv/bin/activate
    python app.py
    exit 0
else
    echo "[INFO] Виртуальное окружение .venv не найдено."
    echo ""
    echo "=== Как создать виртуальное окружение ==="
    echo ""
    echo "[RU]"
    echo "1. Откройте терминал в папке проекта."
    echo "2. Выполните:  python3 -m venv .venv"
    echo "3. Активируйте:  source .venv/bin/activate"
    echo "4. Установите зависимости:  pip install -r requirements.txt"
    echo "5. Запустите игру:  python app.py"
    echo ""
    echo "[EN]"
    echo "1. Open terminal in project folder."
    echo "2. Run:  python3 -m venv .venv"
    echo "3. Activate:  source .venv/bin/activate"
    echo "4. Install dependencies:  pip install -r requirements.txt"
    echo "5. Run game:  python app.py"
    echo ""
    exit 1
fi
