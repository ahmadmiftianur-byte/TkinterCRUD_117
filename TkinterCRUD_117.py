import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "nilai_siswa.db"


def run_query(sql, params=()):
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            return conn.execute(sql, params).fetchall()
    finally:
        conn.close()