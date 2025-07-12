import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import os
from osint_tool import run_osint

# === GUI FUNCTIONALITY ===

def on_run():
    first = entry_first.get().strip()
    last = entry_last.get().strip()
    email = entry_email.get().strip() or None
    phone = entry_phone.get().strip() or None

    if not first or not last:
        messagebox.showerror("Missing Info", "Please enter both First and Last Name.")
        return

    log_box.insert(tk.END, f"[•] Running OSINT on: {first} {last}\n")
    log_box.insert(tk.END, "[•] This may take a moment...\n")
    log_box.see(tk.END)
    root.update()

    try:
        run_osint(first, last, email, phone)
        log_box.insert(tk.END, "[✔] OSINT Scan complete!\n")
        log_box.insert(tk.END, "📂 Results saved in 'results/' folder.\n")
        log_box.see(tk.END)
    except Exception as e:
        log_box.insert(tk.END, f"[!] Error: {e}\n")
        log_box.see(tk.END)

def open_results_folder():
    subprocess.run(["xdg-open", "results"])

# === WINDOW ===

root = tk.Tk()
root.title("Prinsloo OSINT Tool")
root.geometry("560x460")
root.configure(bg="#1f1f1f")

# Set window icon (optional)
try:
    icon_path = "77b0b793-4b59-4052-8b8a-c7691254a443.png"
    root.iconphoto(False, tk.PhotoImage(file=icon_path))
except:
    pass

# === STYLING ===

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", foreground="white", background="#1f1f1f", font=("Segoe UI", 10))
style.configure("TEntry", padding=5)
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)

# === MAIN FRAME ===

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=False)

ttk.Label(frame, text="First Name:").grid(row=0, column=0, sticky="w", pady=5)
entry_first = ttk.Entry(frame, width=30)
entry_first.grid(row=0, column=1, pady=5)

ttk.Label(frame, text="Last Name:").grid(row=1, column=0, sticky="w", pady=5)
entry_last = ttk.Entry(frame, width=30)
entry_last.grid(row=1, column=1, pady=5)

ttk.Label(frame, text="Email (Optional):").grid(row=2, column=0, sticky="w", pady=5)
entry_email = ttk.Entry(frame, width=30)
entry_email.grid(row=2, column=1, pady=5)

ttk.Label(frame, text="Phone (Optional):").grid(row=3, column=0, sticky="w", pady=5)
entry_phone = ttk.Entry(frame, width=30)
entry_phone.grid(row=3, column=1, pady=5)

ttk.Button(frame, text="🔍 Run OSINT Scan", command=on_run).grid(row=4, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="📁 Open Reports Folder", command=open_results_folder).grid(row=5, column=0, columnspan=2)

# === LOG AREA ===

log_box = scrolledtext.ScrolledText(root, height=12, bg="#121212", fg="#00ff99", insertbackground="white", font=("Consolas", 10))
log_box.pack(fill="both", padx=10, pady=(10, 20), expand=True)

# === RUN ===
root.mainloop()

