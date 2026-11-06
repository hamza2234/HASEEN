#!/usr/bin/env python3
"""Launcher: run the desktop application from source.

    python run_app.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from thesis_app.main import main

if __name__ == "__main__":
    raise SystemExit(main())
