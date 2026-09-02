"""
Tkinter Desktop Terminal Interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext

class DigiShellTkApp:
    def __init__(self, root=None):
        self.root = root or tk.Tk()
        self.root.title("DigiShell AI Terminal")
        self.root.geometry("800x500")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, "DigiShell AI Terminal Ready [qwen2.5:3b]\nType your command below:\n\n")

        self.entry = tk.Entry(self.root, bg="#2d2d2d", fg="#ffffff", font=("Consolas", 12))
        self.entry.pack(fill=tk.X, side=tk.BOTTOM)
        self.entry.bind("<Return>", self.on_enter)

    def on_enter(self, event):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self.text_area.insert(tk.END, f"\n> {cmd}\n")
        self.text_area.see(tk.END)

    def run(self):
        self.root.mainloop()

def launch_tkinter():
    app = DigiShellTkApp()
    app.run()
