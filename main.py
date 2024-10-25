
import tkinter as tk
import sqlite3
from tkinter import messagebox

root = tk.Tk()
root.title("PlantTimer v0.0.1")
root.mainloop()

# Try to open DB
# This is copy paste from RandPyPwMan
try:
    conn = sqlite3.connect('./db/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    records = c.fetchall()
except sqlite3.OperationalError:
    # THIS ERROR COULD BE MADE BETTER, IS SQL LITE INSTALLED, OR IS INSTALL.PY NOT RAN? MAKE MORE INFORMATIONAL
    # I.E. DATABASE FOLDER NOT FOUND, PLEASE RUN INSTALL.PY BEFORE EXECUTING PROGRAM
    # OR SQLITE3 NOT FOUND, PLEASE SEE DOCUMENTATION AND INSTALL BEFORE USING PROGRAM
    tkinter.messagebox.showerror(title="SQLite not installed", message="Please install SQLite before use.")
    exit()