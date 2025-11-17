#!/bin/bash

cd /home/admin/beerware || exit 1

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if [ ! -f ".venv/packages_installed.flag" ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .venv/packages_installed.flag
fi

python main.py
