"""
SQL-Magic für Jupyter Notebooks
"""

from IPython.core.magic import register_cell_magic
import sys


def load_sql_magic(connection):
    """Lädt und registriert das %%sql Magic-Kommando für Jupyter.
    
    Args:
        connection (SnowflakeConnection): Eine Instanz von SnowflakeConnection
        
    Returns:
        function: Die registrierte Magic-Funktion
    """
    # Stelle sicher, dass wir in einem IPython/Jupyter-Kontext sind
    try:
        ip = get_ipython()
    except NameError:
        raise RuntimeError("Diese Funktion kann nur in einer IPython-Umgebung verwendet werden.")
    
    # Globale Variable im Benutzernamespace für Ergebnisse
    ip.user_ns['df'] = None
    
    @register_cell_magic
    def sql(line, cell):
        """Magic-Kommando, um SQL-Abfragen direkt auszuführen.
        
        Verwende: %%sql [database_name] in einer Zelle, gefolgt von der SQL-Abfrage.
        Das Ergebnis wird sowohl zurückgegeben als auch in der globalen Variable 'df' gespeichert.
        Unterstützt F-String-Syntax mit Python-Variablen in geschwungenen Klammern {}.
        
        Args:
            line (str): Die erste Zeile nach %%sql (optional: Datenbankname)
            cell (str): Der Inhalt der Zelle (SQL-Abfrage)
            
        Returns:
            pandas.DataFrame: Das Ergebnis der SQL-Abfrage
        """
        # Nutze den globalen result im Benutzernamespace
        database = line.strip() if line.strip() else None
        
        try:
            # F-String-ähnliche Auswertung mit dem Benutzer-Namespace
            formatted_cell = cell.format(**ip.user_ns)
            
            # Debug-Ausgabe, falls gewünscht
            # print(f"SQL nach F-String-Auswertung: {formatted_cell}")
            
            result_df = connection.execute_query(formatted_cell, database)
            ip.user_ns['df'] = result_df
            return result_df
        except KeyError as e:
            print(f"F-String-Fehler: Variable {e} nicht gefunden.", file=sys.stderr)
            ip.user_ns['df'] = None
            return None
        except Exception as e:
            print(f"Fehler bei der Ausführung der SQL-Abfrage: {e}", file=sys.stderr)
            ip.user_ns['df'] = None
            return None
    
    # @register_cell_magic
    # def sql(line, cell):
    #     """Magic-Kommando, um SQL-Abfragen direkt auszuführen.
        
    #     Verwende: %%sql [database_name] in einer Zelle, gefolgt von der SQL-Abfrage.
    #     Das Ergebnis wird sowohl zurückgegeben als auch in der globalen Variable 'result' gespeichert.
        
    #     Args:
    #         line (str): Die erste Zeile nach %%sql (optional: Datenbankname)
    #         cell (str): Der Inhalt der Zelle (SQL-Abfrage)
            
    #     Returns:
    #         pandas.DataFrame: Das Ergebnis der SQL-Abfrage
    #     """
    #     # Nutze den globalen result im Benutzernamespace
    #     database = line.strip() if line.strip() else None
    #     try:
    #         result_df = connection.execute_query(cell, database)
    #         ip.user_ns['df'] = result_df
    #         return result_df
    #     except Exception as e:
    #         print(f"Fehler bei der Ausführung der SQL-Abfrage: {e}", file=sys.stderr)
    #         ip.user_ns['result'] = None
    #         return None
    
    # Magic registrieren
    ip.register_magic_function(sql, 'cell')

    # --- Autovervollständigung für %%sql ---
    def sql_completer(self, event):
        text = event.line
        position = event.end_line_pos
        try:
            cursor = connection.get_cursor()
            # Nach FROM: Schemata vorschlagen
            if text.strip().upper().endswith('FROM'):
                cursor.execute("SHOW SCHEMAS")
                return [row[1] for row in cursor.fetchall()]
            # Nach FROM schema.: Tabellen vorschlagen
            elif '.' in text and 'FROM' in text.upper():
                parts = text.upper().split('FROM')[-1].strip().split('.')
                if len(parts) == 2:
                    schema = parts[0].strip()
                    cursor.execute(f"SHOW TABLES IN SCHEMA {schema}")
                    return [row[1] for row in cursor.fetchall()]
            # Nach table.: Spalten vorschlagen
            elif '.' in text:
                parts = text.strip().split('.')
                if len(parts) >= 2:
                    table = parts[-2].split()[-1]
                    cursor.execute(f"DESCRIBE TABLE {table}")
                    return [row[0] for row in cursor.fetchall()]
        except Exception:
            pass
        # Standard-SQL-Keywords
        return [
            "SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "JOIN", "LEFT JOIN", "INNER JOIN", "LIMIT", "OFFSET"
        ]

    # Completer für %%sql registrieren
    if hasattr(ip, 'set_hook'):
        ip.set_hook('complete_command', sql_completer, re_key='.*%sql.*')

    print("SQL-Magic wurde aktiviert. Du kannst jetzt %%sql [database] in Zellen verwenden.")
    print("Das Abfrageergebnis wird in der globalen Variable 'df' gespeichert.")
    
    return #sql
