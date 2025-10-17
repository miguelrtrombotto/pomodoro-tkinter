import tkinter as tk
from tkinter import ttk

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador Pomodoro")
        self.root.geometry("360x300")
        self.root.resizable(False, False)

        # Variables UI iniciales
        self.work_min = tk.IntVar(value=25)
        self.break_min = tk.IntVar(value=5)
        self.phase_var = tk.StringVar(value="Trabajo")
        self.time_var = tk.StringVar(value="25:00")  # Solo display en Issue 1

        # Construcción de UI
        self._build_ui()

        # Estados iniciales de botones (Issue 1: solo interfaz)
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.reset_btn.config(state="disabled")

    def _build_ui(self):
        pad = 8

        # Frame de configuración
        cfg = ttk.LabelFrame(self.root, text="Configuración")
        cfg.pack(fill="x", padx=pad, pady=(pad, 0))

        ttk.Label(cfg, text="Trabajo (min):").grid(row=0, column=0, padx=4, pady=4, sticky="e")
        ttk.Spinbox(cfg, from_=1, to=180, textvariable=self.work_min, width=5).grid(row=0, column=1, padx=4, pady=4, sticky="w")

        ttk.Label(cfg, text="Descanso (min):").grid(row=0, column=2, padx=4, pady=4, sticky="e")
        ttk.Spinbox(cfg, from_=1, to=60, textvariable=self.break_min, width=5).grid(row=0, column=3, padx=4, pady=4, sticky="w")

        # Display de fase y tiempo
        disp = ttk.Frame(self.root)
        disp.pack(fill="x", padx=pad, pady=pad)
        ttk.Label(disp, textvariable=self.phase_var, font=("Segoe UI", 12, "bold")).pack(pady=(4, 0))
        ttk.Label(disp, textvariable=self.time_var, font=("Consolas", 36, "bold")).pack(pady=(0, 4))

        # Botones principales (sin lógica en Issue 1)
        btns = ttk.Frame(self.root)
        btns.pack(padx=pad, pady=pad)
        self.start_btn = ttk.Button(btns, text="Iniciar", command=lambda: None)   # placeholder
        self.start_btn.grid(row=0, column=0, padx=4, pady=4)
        self.pause_btn = ttk.Button(btns, text="Pausar", command=lambda: None)   # placeholder
        self.pause_btn.grid(row=0, column=1, padx=4, pady=4)
        self.reset_btn = ttk.Button(btns, text="Reiniciar", command=lambda: None) # placeholder
        self.reset_btn.grid(row=0, column=2, padx=4, pady=4)

def main():
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()