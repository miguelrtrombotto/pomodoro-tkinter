import tkinter as tk
from tkinter import ttk

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Temporizador Pomodoro")
        self.root.geometry("360x300")
        self.root.resizable(False, False)

        # Variables UI
        self.work_min = tk.IntVar(value=00)
        self.break_min = tk.IntVar(value=0)
        self.phase_var = tk.StringVar(value="Trabajo")
        self.time_var = tk.StringVar(value="00:00")  # display inicial

        # Estado del temporizador
        self.is_running = False
        self.is_break = False  # False = Trabajo, True = Descanso
        self.remaining_secs = 00
        self._after_id = None

        # Construcción de UI
        self._build_ui()
        # Atajos de teclado (Issue 3)
        self._bind_shortcuts()

        # Fase inicial y render
        self._set_phase(work=True, reset_remaining=False)
        self._update_buttons(start=True, pause=False, reset=False)

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

        # Botones (Issue 3: funcionales)
        btns = ttk.Frame(self.root)
        btns.pack(padx=pad, pady=pad)
        self.start_btn = ttk.Button(btns, text="Iniciar", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=4, pady=4)
        self.pause_btn = ttk.Button(btns, text="Pausar", command=self.pause_timer)
        self.pause_btn.grid(row=0, column=1, padx=4, pady=4)
        self.reset_btn = ttk.Button(btns, text="Reiniciar", command=self.reset_timer)
        self.reset_btn.grid(row=0, column=2, padx=4, pady=4)

    # ===== Atajos (Issue 3) =====
    def _bind_shortcuts(self):
        # Espacio: toggle iniciar/pausar
        self.root.bind("<space>", lambda e: self._toggle_start_pause())
        # Ctrl+R: reiniciar
        self.root.bind("<Control-r>", lambda e: self.reset_timer())

    def _toggle_start_pause(self):
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()

    # ===== Utilidades UI =====
    def _update_buttons(self, start: bool, pause: bool, reset: bool):
        self.start_btn.config(state="normal" if start else "disabled")
        self.pause_btn.config(state="normal" if pause else "disabled")
        self.reset_btn.config(state="normal" if reset else "disabled")

    # ===== Lógica del temporizador =====
    def _render_time(self):
        m, s = divmod(max(0, int(self.remaining_secs)), 60)
        self.time_var.set(f"{m:02d}:{s:02d}")

    def _set_phase(self, work: bool, reset_remaining: bool):
        self.is_break = not work
        self.phase_var.set("Descanso" if self.is_break else "Trabajo")
        if reset_remaining:
            minutes = self.break_min.get() if self.is_break else self.work_min.get()
            self.remaining_secs = int(minutes) * 60
        self._render_time()
        
    def _tick(self):
        if not self.is_running:
            return
        self.remaining_secs -= 1
        self._render_time()
        if self.remaining_secs <= 0:
            self._phase_finished()
            return
        self._after_id = self.root.after(1000, self._tick)

    def _phase_finished(self):
        # Alerta al terminar la fase
        try:
            self.root.bell()
        except Exception:
            # En algunos entornos (p. ej., ciertos Windows/remoto) puede no estar disponible
            pass

        # Alternar automáticamente Trabajo <-> Descanso
        if self.is_break:
            # Terminó Descanso -> vuelve a Trabajo
            self._set_phase(work=True, reset_remaining=True)
        else:
            # Terminó Trabajo -> pasa a Descanso
            self._set_phase(work=False, reset_remaining=True)

        # Seguir corriendo automáticamente
        self._after_id = self.root.after(1000, self._tick)
    
    # ===== Controles (Issue 3) =====
    def start_timer(self):
        if self.is_running:
            return
        # Si el contador está en 0 (por pruebas previas), rearmar siguiente fase coherente
        if self.remaining_secs <= 0:
            self._set_phase(work=not self.is_break, reset_remaining=True)
        self.is_running = True
        self._update_buttons(start=False, pause=True, reset=True)
        self._tick()

    def pause_timer(self):
        if not self.is_running:
            return
        self.is_running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        self._update_buttons(start=True, pause=False, reset=True)

    def reset_timer(self):
        # Parar si está corriendo
        self.is_running = False
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        # Volver a Trabajo con el tiempo configurado
        self._set_phase(work=True, reset_remaining=True)
        self._update_buttons(start=True, pause=False, reset=False)

def main():
    root = tk.Tk()
    PomodoroApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()