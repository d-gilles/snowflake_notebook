# Snowflake Notebook

Ein einfaches Paket für die Integration von Snowflake mit Jupyter Notebooks.

## Installation

```bash
pip install .
```

## Verwendung

```python
# In deinem Jupyter Notebook
from snowflake_notebook import SnowflakeConnection, load_sql_magic

# Konfiguration aus .env-Datei laden oder direkt angeben
conn = SnowflakeConnection.from_env()
# Oder:
# conn = SnowflakeConnection(user="user", password="pwd", account="account", ...)

# SQL-Magic aktivieren
load_sql_magic(conn)

# Jetzt kannst du SQL direkt in Zellen ausführen:
# %%sql [database_name]
# SELECT * FROM my_table
```

## Features

- Einfache Verbindung zu Snowflake
- SQL-Magic für direkte SQL-Ausführung in Jupyter-Zellen
- Automatische Speicherung des letzten Abfrageergebnisses in der `result`-Variable
