# Data Analyst Chatbot

This is a beginner-friendly local chatbot that helps you analyze CSV datasets from the command line.
It uses local Python (pandas) for common data-analysis actions and optionally calls an LLM (OpenAI) for natural-language explanations and complex requests.

## Features
- Load a CSV and inspect data (head, columns, describe)
- Ask simple data questions that can be answered locally (e.g., top values, sums, group-by)
- Generate Python or SQL snippets to reproduce analyses
- Optional: use OpenAI API for natural-language answers (requires API key)

## Files
- `app.py` - main CLI chatbot application
- `utils.py` - helper functions for local analysis and formatting
- `sample.csv` - sample dataset to try the bot (sales demo)
- `requirements.txt` - Python packages required
- `README.md` - this file

