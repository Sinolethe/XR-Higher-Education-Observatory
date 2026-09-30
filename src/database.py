# src/database.py

import sqlite3

DB_PATH = "database/xr_observatory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)

