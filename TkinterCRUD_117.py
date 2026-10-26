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

def init_db():
    run_query("""CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
    )""")

def simpan_nilai(nama, biologi, fisika, inggris, prediksi):
    run_query("""INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)""",
        (nama, biologi, fisika, inggris, prediksi))

def get_students():
    return run_query("""SELECT nama_siswa, biologi, fisika,
        inggris, prediksi_fakultas FROM nilai_siswa""")


def delete_student(nama, biologi, fisika, inggris, prediksi):
    run_query("""DELETE FROM nilai_siswa
        WHERE nama_siswa = ? AND biologi = ?
        AND fisika = ? AND inggris = ?
        AND prediksi_fakultas = ?""",
        (nama, biologi, fisika, inggris, prediksi))

init_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("700x550")


# Membuat input
entries = {}

for i, field in enumerate(["Nama Siswa", "Biologi", "Fisika", "Inggris"]):
    tk.Label(root, text=field).grid(row=i, column=0, pady=5)
    entries[field] = tk.Entry(root, width=25)
    entries[field].grid(row=i, column=1, pady=5)