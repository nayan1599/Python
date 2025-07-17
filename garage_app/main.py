import tkinter as tk
from tkinter import messagebox
import subprocess

def open_module(filename):
    try:
        subprocess.Popen(["python", filename])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open {filename}\n\n{e}")

def on_enter(e):
    e.widget['bg'] = '#375a7f'
def on_leave(e):
    e.widget['bg'] = '#2c3e50'

root = tk.Tk()
root.title("🚗 Garage Management System - Admin Dashboard")
root.geometry("700x450")
root.minsize(700, 450)

# Sidebar Frame
sidebar = tk.Frame(root, bg="#2c3e50", width=200)
sidebar.pack(side="left", fill="y")

# Header on Sidebar
header = tk.Label(sidebar, text="Admin Panel", bg="#1a252f", fg="white", font=("Helvetica", 18, "bold"), pady=20)
header.pack(fill="x")

# Buttons on Sidebar
buttons = [
    ("Vehicle Management", "vehicle.py", "🚗"),
    ("Customer Management", "customer.py", "👤"),
    ("Rental System", "rental.py", "📅"),
    ("Installment System", "installment.py", "💰"),
    ("Payment Receive", "payment.py", "💳"),
    ("Reports", "reports/today_rentals.py", "📊"),
]

for (text, file, emoji) in buttons:
    btn = tk.Button(sidebar, text=f"{emoji}  {text}", font=("Arial", 12), bg="#2c3e50", fg="white", bd=0,
                    activebackground="#375a7f", activeforeground="white", anchor="w",
                    command=lambda f=file: open_module(f))
    btn.pack(fill="x", padx=10, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Exit button at bottom
exit_btn = tk.Button(sidebar, text="❌ Exit", font=("Arial", 12), bg="#c0392b", fg="white", bd=0,
                     activebackground="#e74c3c", command=root.destroy)
exit_btn.pack(side="bottom", fill="x", padx=10, pady=20)

# Main Content Area (for future expansion)
main_content = tk.Frame(root, bg="white")
main_content.pack(expand=True, fill="both")

welcome_label = tk.Label(main_content, text="Welcome to Garage Management System", font=("Helvetica", 20), bg="white")
welcome_label.pack(pady=100)

root.mainloop()
