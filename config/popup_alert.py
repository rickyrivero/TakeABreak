import tkinter as tk
from tkinter import messagebox

def show_popup(title, message):
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showinfo(title, message)
    root.destroy()  # Cierra el popup limpio
