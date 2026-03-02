import os
import sqlite3
from typing import Optional

from config.project import yaml_config


class SqliteManager:
    _connection: Optional[sqlite3.Connection] = None

    def connect(self):
        if self._connection is not None:
            try:
                self._connection.execute("SELECT 1")
                return self._connection
            except sqlite3.Error:
                self._connection = None

        excel_db_path = yaml_config.excel_db_path
        if excel_db_path is None:
            raise Exception("excel_db_path,请在config.yaml中进行配置!!")

        sqlite_path = os.path.join(excel_db_path, "ExcelDB.db")
        self._connection = sqlite3.connect(sqlite_path, check_same_thread=False)
        self._connection.row_factory = sqlite3.Row
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    @property
    def cursor(self):
        if self._connection is None:
            self.connect()

        return self._connection.cursor()  # type: ignore


excel_db = SqliteManager()
