# Snowflake Notebook Beispiele

In diesem Verzeichnis findest du Beispiele für die Verwendung der `snowflake_notebook` Bibliothek.

## Dateien

- `basic_usage.py`: Ein einfaches Python-Skript, das die grundlegende Verwendung zeigt
- `example_notebook.ipynb`: Ein Jupyter Notebook mit Beispielen für die Verwendung der SQL-Magic-Funktionalität

## Verwendung

1. Installiere zuerst die Bibliothek:
   ```
   pip install -e ..
   ```
   
2. Erstelle eine `.env`-Datei mit deinen Snowflake-Zugangsdaten:
   ```
   user_dev=DEIN_BENUTZER
   pwd_dev=DEIN_PASSWORT
   account=DEIN_ACCOUNT
   warehouse=DEIN_WAREHOUSE
   database=DEINE_DB
   ```
   
3. Führe die Beispiele aus:
   - Python-Skript: `python basic_usage.py`
   - Notebook: Öffne `example_notebook.ipynb` in Jupyter oder VS Code
