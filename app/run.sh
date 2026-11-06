#!/usr/bin/env bash
# Launch the thesis demo web app on port 12000.
set -u
cd "$(dirname "$0")"

PORT="${PORT:-12000}"

if ! python3 -c "import flask, sklearn, pandas, numpy, openpyxl" 2>/dev/null; then
  echo "Installing dependencies..."
  python3 -m pip install -q -r requirements.txt
fi

echo "Starting server on http://0.0.0.0:${PORT}"
exec python3 app.py
