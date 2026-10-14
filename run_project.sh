#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ ! -f ".venv/bin/activate" ]]; then
    echo "Virtual environment not found at .venv/bin/activate."
    echo "Create it first with: python3 -m venv .venv"
    exit 1
fi

echo "Activating virtual environment..."
source ".venv/bin/activate"
echo "Virtual environment activated."

read -r -p "Train the model now? This can take a long time and benefits from a GPU. [y/N] " REPLY
if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    echo "Starting model training..."
    python train.py
else
    echo "Skipped model training."
fi

echo "Starting Django development server..."
cd spam_detector
python manage.py runserver
