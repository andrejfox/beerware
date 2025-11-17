#!/bin/bash

cd /home/admin/beerware || exit 1

source .venv/bin/activate

# Install deps ONLY if not already installed
if [ ! -f ".venv/packages_installed.flag" ]; then
    pip install -r requirements.txt
    touch .venv/packages_installed.flag
fi

python main.py
