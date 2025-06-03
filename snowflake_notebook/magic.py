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
    ip.user_ns['result'] = None
    
    @register_cell_magic
    def sql(line, cell):
        """Magic-Kommando, um SQL-Abfragen direkt auszuführen.
        
        Verwende: %%sql [database_name] in einer Zelle, gefolgt von der SQL-Abfrage.
        Das Ergebnis wird sowohl zurückgegeben als auch in der globalen Variable 'result' gespeichert.
        
        Args:
            line (str): Die erste Zeile nach %%sql (optional: Datenbankname)
            cell (str): Der Inhalt der Zelle (SQL-Abfrage)
            
        Returns:
            pandas.DataFrame: Das Ergebnis der SQL-Abfrage
        """
        # Nutze den globalen result im Benutzernamespace
        database = line.strip() if line.strip() else None
        result_df = connection.execute_query(cell, database)
        ip.user_ns['result'] = result_df
        return result_df
    
    # Magic registrieren
    ip.register_magic_function(sql, 'cell')
    
    print("SQL-Magic wurde aktiviert. Du kannst jetzt %%sql [database] in Zellen verwenden.")
    print("Das Abfrageergebnis wird in der globalen Variable 'result' gespeichert.")
    
    return sql
