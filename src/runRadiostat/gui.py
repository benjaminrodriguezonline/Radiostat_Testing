import tkinter as tk
from tkinter import messagebox
from runRadiostat.dummy_test import run_dummy_test
from runRadiostat.beaker_test import run_beaker_test

def launch_gui():
    def on_run_click():
        try:
            run_dummy_test()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def on_beaker_click():
        try:
            run_beaker_test()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

    window = tk.Tk()
    window.title("Radiostat: Dummy Cell Check")
    window.geometry("300x150")

    label = tk.Label(window, text="Check Rodeostat connection")
    label.pack(pady=10)

    run_button = tk.Button(window, text="Run Dummy Test", command=on_run_click)
    run_button.pack(pady=10)

    beaker_button = tk.Button(window, text="Run Beaker Test", command=on_beaker_click)
    beaker_button.pack(pady=10)

    window.mainloop()