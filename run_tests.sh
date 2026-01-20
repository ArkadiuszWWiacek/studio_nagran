#!/bin/bash

set -e  # Zatrzymaj na błędzie

echo "Uruchamianie testów pytest..."
pytest tests/ -v --cov=app --cov-report=term-missing || { echo "Pytest nieudany!"; exit 1; }

echo "Uruchamianie pylint..."
pylint ./ || { echo "Pylint nieudany!"; exit 2; }

echo "Wszystko OK!"
    