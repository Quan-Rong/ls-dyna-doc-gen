#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CLI Application Entry Point

This is the main entry point for the CLI (Command Line Interface) application.
The actual business logic is in cli_main.py.

Usage:
    python cli_app/main.py                    # Process all files in Input/ directory
    python cli_app/main.py file.key           # Process specific file
    python cli_app/main.py --force            # Force regenerate all files
"""

from cli_app.cli_main import main

if __name__ == "__main__":
    main()
