"""
Verbindungsklasse für Snowflake
"""

import os
import pandas as pd
from snowflake.connector import connect
import dotenv


class SnowflakeConnection:
    """Eine Klasse zur Verwaltung der Verbindung zu Snowflake."""
    
    def __init__(self, user, password, account, warehouse, database=None):
        """Initialisiert eine neue Verbindung zu Snowflake.
        
        Args:
            user (str): Benutzername für Snowflake
            password (str): Passwort für Snowflake
            account (str): Snowflake Account-Identifier
            warehouse (str): Zu verwendender Snowflake Warehouse
            database (str, optional): Zu verwendende Standard-Datenbank
        """
        self.conn = connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database if database else None
        )
        self.current_database = database
        
    @classmethod
    def from_env(cls, env_file=None):
        """Erstellt eine Verbindung aus Umgebungsvariablen oder einer .env-Datei.
        
        Args:
            env_file (str, optional): Pfad zur .env-Datei. Wenn None, wird nach .env im aktuellen Verzeichnis gesucht.
            
        Returns:
            SnowflakeConnection: Eine neue Verbindungsinstanz
            
        Beispiel für eine .env-Datei:
            user_dev=MEIN_BENUTZER
            pwd_dev=MEIN_PASSWORT
            account=MEIN_ACCOUNT
            warehouse=MEIN_WAREHOUSE
            database=MEINE_DB
        """
        if env_file:
            dotenv.load_dotenv(env_file)
        else:
            dotenv.load_dotenv()
            
        user = os.getenv("user_dev")
        password = os.getenv("pwd_dev")
        account = os.getenv("account")
        warehouse = os.getenv("warehouse")
        database = os.getenv("database")
        
        if not all([user, password, account, warehouse]):
            raise ValueError("Nicht alle erforderlichen Umgebungsvariablen sind gesetzt.")
            
        return cls(user, password, account, warehouse, database)
        
    def execute_query(self, query, database=None):
        """Führt eine SQL-Abfrage aus und gibt die Ergebnisse als DataFrame zurück.
        
        Args:
            query (str): Die auszuführende SQL-Abfrage
            database (str, optional): Optional eine andere Datenbank zu verwenden
            
        Returns:
            pandas.DataFrame: Die Ergebnisse der Abfrage als DataFrame
        """
        with self.conn.cursor() as cursor:
            if database:
                cursor.execute(f"USE DATABASE {database}")
                self.current_database = database
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
    
    def use_database(self, database):
        """Wechselt die aktuelle Datenbank.
        
        Args:
            database (str): Name der zu verwendenden Datenbank
        """
        with self.conn.cursor() as cursor:
            cursor.execute(f"USE DATABASE {database}")
        self.current_database = database
    
    def close(self):
        """Schließt die Verbindung zu Snowflake."""
        self.conn.close()
