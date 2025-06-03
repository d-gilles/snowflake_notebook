# Beispielcode für die Verwendung von snowflake_notebook

# 1. Importieren der Bibliothek
from snowflake_notebook import SnowflakeConnection, load_sql_magic

# 2. Verbindung herstellen (aus .env-Datei oder direkt)
# Methode 1: Aus .env-Datei
conn = SnowflakeConnection.from_env()

# Methode 2: Direkte Angabe
# conn = SnowflakeConnection(
#     user="DEIN_BENUTZER", 
#     password="DEIN_PASSWORT",
#     account="DEIN_ACCOUNT",
#     warehouse="DEIN_WAREHOUSE",
#     database="DEINE_DB"  # Optional
# )

# 3. SQL-Magic aktivieren
load_sql_magic(conn)

# 4. Jetzt kann SQL direkt in Zellen verwendet werden:
# %%sql
# SELECT * FROM meine_tabelle

# 5. Oder mit Datenbankangabe:
# %%sql andere_datenbank
# SELECT * FROM andere_tabelle

# 6. Das Ergebnis der letzten Abfrage ist in der Variable 'result' verfügbar
# result.head()

# 7. Es können auch Methoden der Verbindung direkt verwendet werden
df = conn.execute_query("SELECT 1 AS test")
print(df)

# 8. Verbindung schließen, wenn nicht mehr benötigt
# conn.close()
