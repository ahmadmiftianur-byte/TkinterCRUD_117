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


def submit_nilai():
    nama = entries["Nama Siswa"].get().strip()
    biologi = entries["Biologi"].get().strip()
    fisika = entries["Fisika"].get().strip()
    inggris = entries["Inggris"].get().strip()

    if not nama or not biologi or not fisika or not inggris:
        messagebox.showwarning("Peringatan", "Semua data harus diisi!")
        return

    if not biologi.isdigit() or not fisika.isdigit() or not inggris.isdigit():
        messagebox.showwarning("Peringatan", "Nilai harus berupa angka!")
        return

    biologi = int(biologi)
    fisika = int(fisika)
    inggris = int(inggris)

    if biologi > fisika and biologi > inggris:
        prediksi = "Kedokteran"

    elif fisika > biologi and fisika > inggris:
        prediksi = "Teknik"

    elif inggris > biologi and inggris > fisika:
        prediksi = "Bahasa"

    else:
        messagebox.showinfo("Hasil", "Nilai tertinggi sama!")
        return

    simpan_nilai(nama, biologi, fisika, inggris, prediksi)

    hasil.config(text="Prediksi Fakultas: " + prediksi)

    messagebox.showinfo("Berhasil", "Data berhasil disimpan!")

    for e in entries.values():
        e.delete(0, tk.END)

    refresh()


def refresh():
    tree.delete(*tree.get_children())

    for row in get_students():
        tree.insert("", tk.END, values=row)


def on_select(event):
    selected_item = tree.selection()

    if selected_item:
        data = tree.item(selected_item[0], "values")
        hasil.config(text="Prediksi Fakultas: " + data[4])


# Membuat tabel
cols = ("nama_siswa", "biologi", "fisika",
        "inggris", "prediksi_fakultas")

tree = ttk.Treeview(root, columns=cols, show="headings")

for col in cols:
    tree.heading(col, text=col.title())

tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", on_select)


# Tombol submit
tombol = tk.Button(
    root,
    text="Submit Nilai",
    command=submit_nilai
)
tombol.grid(row=5, column=0, pady=10)


# Fungsi hapus data
def hapus_data():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return

    data = tree.item(selected_item[0], "values")

    delete_student(
        data[0],
        data[1],
        data[2],
        data[3],
        data[4]
    )

    refresh()

    hasil.config(text="Hasil Prediksi: -")

    messagebox.showinfo("Berhasil", "Data berhasil dihapus!")


# Tombol hapus
tombol_hapus = tk.Button(
    root,
    text="Hapus Data",
    command=hapus_data
)
tombol_hapus.grid(row=5, column=1, pady=10)


# Menampilkan hasil
hasil = tk.Label(root, text="Hasil Prediksi: -")
hasil.grid(row=6, column=0, columnspan=2)


refresh()
root.mainloop()