import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import time

class AppLauncherUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Guten Morgen Launcher")
        self.root.configure(bg="#8F8F8F")
        self.program_paths = []
        self.click_position = None  # Gespeicherte Klickposition

        frame = tk.Frame(root, padx=20, pady=20, bg="#8F8F8F")
        frame.pack()

        font_label = ("Arial", 12, "bold")

        self.label = tk.Label(frame, text="Programme auswählen:", font=font_label, bg="#8F8F8F")
        self.label.grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="w")

        button_style = {
            "width": 25,  # Hier nur einmal width definieren!
            "bg": "#007acc",
            "fg": "white",
            "activebackground": "#005f99",
            "font": ("Arial", 10, "bold"),
            "relief": "raised",
            "bd": 2,
        }

        self.select_button = tk.Button(frame, text="Programm hinzufügen", command=self.add_program, **button_style)
        self.select_button.grid(row=1, column=0, padx=5, pady=5)

        self.remove_button = tk.Button(frame, text="Ausgewähltes entfernen", command=self.remove_selected, **button_style)
        self.remove_button.grid(row=1, column=1, padx=5, pady=5)

        self.start_button = tk.Button(frame, text="Alle Programme starten", command=self.start_programs, **button_style)
        self.start_button.grid(row=1, column=2, padx=5, pady=5)

        self.save_button = tk.Button(frame, text="Speichern", command=self.save_programs, **button_style)
        self.save_button.grid(row=1, column=3, padx=5, pady=5)

        self.delay_label = tk.Label(frame, text="Verzögerung (Sekunden):", font=font_label, bg="#8F8F8F")
        self.delay_label.grid(row=2, column=0, sticky="e", pady=(10, 0), padx=(0, 5))

        self.delay_entry = tk.Entry(frame, width=5, font=("Arial", 10))
        self.delay_entry.insert(0, "1")
        self.delay_entry.grid(row=2, column=1, sticky="w", pady=(10, 0))

        # Klickposition merken + Verzögerung Label in einer Zeile
        self.pos_button = tk.Button(frame, text="Klickposition merken (5 Sek.)", command=self.remember_click_position, **button_style)
        self.pos_button.grid(row=2, column=2, padx=5, pady=(10,0))

        self.pos_label = tk.Label(frame, text="Klickposition noch nicht gesetzt", font=("Arial", 10), bg="#8F8F8F")
        self.pos_label.grid(row=2, column=3, sticky="w", pady=(10,0), padx=(5,0))

        list_frame = tk.Frame(frame, bg="#8F8F8F")
        list_frame.grid(row=3, column=0, columnspan=4, pady=15, sticky="nsew")

        self.listbox = tk.Listbox(list_frame, width=100, height=12, font=("Arial", 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.quit_button = tk.Button(frame, text="Beenden", command=root.quit, **button_style)
        self.quit_button.grid(row=4, column=1, columnspan=2, pady=10)

        for i in range(4):
            frame.grid_columnconfigure(i, weight=1)

        self.load_programs()
        self.load_click_position()

    def add_program(self):
        filepath = filedialog.askopenfilename(title="Programm auswählen", filetypes=[("Alle Dateien", "*.*")])
        if filepath:
            if filepath not in self.program_paths:
                self.program_paths.append(filepath)
                self.listbox.insert(tk.END, filepath)
            else:
                messagebox.showinfo("Hinweis", "Programm ist schon in der Liste.")

    def remove_selected(self):
        selected_idx = self.listbox.curselection()
        if not selected_idx:
            messagebox.showinfo("Hinweis", "Bitte erst ein Programm in der Liste auswählen.")
            return
        index = selected_idx[0]
        self.listbox.delete(index)
        del self.program_paths[index]

    def start_programs(self):
        if not self.program_paths:
            messagebox.showinfo("Hinweis", "Keine Programme zum Starten ausgewählt.")
            return

        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Fehler", "Bitte eine gültige positive Zahl für die Verzögerung eingeben.")
            return

        for path in self.program_paths:
            try:
                if os.path.exists(path):
                    subprocess.Popen(path)
                    time.sleep(delay)
                    # Falls Klickposition gesetzt, Mausklick ausführen:
                    if self.click_position:
                        self.perform_click(self.click_position)
                else:
                    messagebox.showwarning("Fehler", f"Pfad existiert nicht:\n{path}")
            except Exception as e:
                messagebox.showerror("Fehler beim Starten", f"{path}\n\n{e}")

    def perform_click(self, position):
        # Klick ausführen an gegebener Position (x,y)
        try:
            import pyautogui
            pyautogui.click(position[0], position[1])
        except ImportError:
            messagebox.showerror("Fehler", "pyautogui-Modul ist nicht installiert.\nInstalliere es mit:\npip install pyautogui")

    def remember_click_position(self):
        self.pos_label.config(text="Klicke in 5 Sekunden an gewünschte Position...")
        self.root.update()
        time.sleep(5)
        try:
            import pyautogui
            x, y = pyautogui.position()
            self.click_position = (x, y)
            self.pos_label.config(text=f"Klickposition gesetzt: {x}, {y}")
            self.save_click_position()
        except ImportError:
            messagebox.showerror("Fehler", "pyautogui-Modul ist nicht installiert.\nInstalliere es mit:\npip install pyautogui")

    def save_programs(self):
        try:
            with open("programs.txt", "w", encoding="utf-8") as f:
                for path in self.program_paths:
                    f.write(path + "\n")
            messagebox.showinfo("Erfolg", "Programme erfolgreich gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen:\n{e}")

    def load_programs(self):
        if os.path.exists("programs.txt"):
            try:
                with open("programs.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        path = line.strip()
                        if path and path not in self.program_paths:
                            self.program_paths.append(path)
                            self.listbox.insert(tk.END, path)
            except Exception as e:
                messagebox.showerror("Fehler beim Laden", f"Programme konnten nicht geladen werden:\n{e}")

    def save_click_position(self):
        try:
            with open("click_position.txt", "w") as f:
                if self.click_position:
                    f.write(f"{self.click_position[0]},{self.click_position[1]}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Klickposition konnte nicht gespeichert werden:\n{e}")

    def load_click_position(self):
        if os.path.exists("click_position.txt"):
            try:
                with open("click_position.txt", "r") as f:
                    line = f.readline().strip()
                    if line:
                        x_str, y_str = line.split(",")
                        self.click_position = (int(x_str), int(y_str))
                        self.pos_label.config(text=f"Klickposition geladen: {self.click_position[0]}, {self.click_position[1]}")
            except Exception as e:
                messagebox.showerror("Fehler", f"Klickposition konnte nicht geladen werden:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.attributes("-topmost", True)
    app = AppLauncherUI(root)
    root.mainloop()
