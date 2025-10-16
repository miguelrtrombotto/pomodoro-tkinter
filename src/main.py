import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Temporizador Pomodoro")
    root.geometry("360x300")
    ttk.Label(root, text="Pomodoro — Preparando MVP").pack(pady=40)
    root.mainloop()

if __name__ == "__main__":
    main()