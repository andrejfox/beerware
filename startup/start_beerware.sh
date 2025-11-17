#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR" || exit 1
echo "Current project directory: $PROJECT_DIR"

if [ ! -d ".venv" ]; then
    echo -e "\e[32mCreating virtual environment...\e[0m"
    python3 -m venv .venv
fi

source .venv/bin/activate

if [ ! -f ".venv/packages_installed.flag" ]; then
    echo -e "\e[32mInstalling Python packages...\e[0m"
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .venv/packages_installed.flag
fi

./.venv/bin/python main.py
