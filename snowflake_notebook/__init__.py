"""
Snowflake Notebook - Ein Paket für die einfache Integration von Snowflake mit Jupyter Notebooks
"""

from snowflake_notebook.connection import SnowflakeConnection
from snowflake_notebook.magic import load_sql_magic

__all__ = ["SnowflakeConnection", "load_sql_magic"]
