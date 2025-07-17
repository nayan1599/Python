import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime

def add_customer():
    first_name = entry_first_name.get().strip()
    last_name = entry_last_name.get().strip()
    gender = gender_var.get()
    dob = entry_dob.get().strip()
    phone = entry_phone.get().strip()
    email = entry_email.get().strip()
    address = text_address.get("1.0", tk.END).strip()
    city = entry_city.get().strip()
    state = entry_state.get().strip()
    postal_code = entry_postal.get().strip()
    country = entry_country.get().strip()
    national_id = entry_nid.get().strip()
    occupation = entry_occupation.get().strip()
    customer_type = customer_type_var.get()
    notes = text_notes.get("1.0", tk.END).strip()
    status = status_var.get()

    if not first_name or not last_name or not phone:
        messagebox.showwarning("সতর্কতা", "প্রথম নাম, শেষ নাম এবং ফোন নম্বর অবশ্যই পূরণ করুন।")
        return

    if dob:
        try:
            datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("ভুল ফরম্যাট", "জন্ম তারিখ yyyy-mm-dd ফরম্যাটে দিন (যেমন 1990-12-31)")
            return

    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO customers 
            (first_name, last_name, gender, date_of_birth, phone, email, address, city, state, postal_code, country, national_id, occupation, customer_type, notes, status) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, gender, dob, phone, email, address, city, state, postal_code, country, national_id, occupation, customer_type, notes, status))
        conn.commit()
        messagebox.showinfo("সাফল্য", "কাস্টমার সফলভাবে যোগ করা হয়েছে।")
        clear_form()
        load_customers()
    except Exception as e:
        messagebox.showerror("ত্রুটি", f"কাস্টমার সংরক্ষণে ব্যর্থ: {str(e)}")
    finally:
        conn.close()

def load_customers():
    for item in tree.get_children():
        tree.delete(item)

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, gender, phone, email, city, customer_type, status FROM customers ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

def clear_form():
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    gender_var.set('পুরুষ')
    entry_dob.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    text_address.delete("1.0", tk.END)
    entry_city.delete(0, tk.END)
    entry_state.delete(0, tk.END)
    entry_postal.delete(0, tk.END)
    entry_country.delete(0, tk.END)
    entry_nid.delete(0, tk.END)
    entry_occupation.delete(0, tk.END)
    customer_type_var.set('ক্রেতা')
    text_notes.delete("1.0", tk.END)
    status_var.set('Active')

root = tk.Tk()
root.title("👤 কাস্টমার ব্যবস্থাপনা")
root.geometry("950x650")

form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack(fill=tk.X)

# Row 0
tk.Label(form_frame, text="প্রথম নাম:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
entry_first_name = tk.Entry(form_frame, font=("Arial", 12))
entry_first_name.grid(row=0, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="শেষ নাম:", font=("Arial", 12)).grid(row=0, column=2, sticky="e", pady=5)
entry_last_name = tk.Entry(form_frame, font=("Arial", 12))
entry_last_name.grid(row=0, column=3, pady=5, sticky="w")

# Row 1
tk.Label(form_frame, text="লিঙ্গ:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
gender_var = tk.StringVar(value='পুরুষ')
gender_options = ttk.Combobox(form_frame, textvariable=gender_var,
                              values=['পুরুষ', 'মহিলা', 'অন্যান্য'], state="readonly", width=18)
gender_options.grid(row=1, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="জন্ম তারিখ (yyyy-mm-dd):", font=("Arial", 12)).grid(row=1, column=2, sticky="e", pady=5)
entry_dob = tk.Entry(form_frame, font=("Arial", 12))
entry_dob.grid(row=1, column=3, pady=5, sticky="w")

# Row 2
tk.Label(form_frame, text="ফোন:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
entry_phone = tk.Entry(form_frame, font=("Arial", 12))
entry_phone.grid(row=2, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ইমেইল:", font=("Arial", 12)).grid(row=2, column=2, sticky="e", pady=5)
entry_email = tk.Entry(form_frame, font=("Arial", 12))
entry_email.grid(row=2, column=3, pady=5, sticky="w")

# Row 3
tk.Label(form_frame, text="ঠিকানা:", font=("Arial", 12)).grid(row=3, column=0, sticky="ne", pady=5)
text_address = tk.Text(form_frame, width=35, height=3, font=("Arial", 12))
text_address.grid(row=3, column=1, pady=5, sticky="w")

# Row 4
tk.Label(form_frame, text="শহর:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", pady=5)
entry_city = tk.Entry(form_frame, font=("Arial", 12))
entry_city.grid(row=4, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="জেলা:", font=("Arial", 12)).grid(row=4, column=2, sticky="e", pady=5)
entry_state = tk.Entry(form_frame, font=("Arial", 12))
entry_state.grid(row=4, column=3, pady=5, sticky="w")

# Row 5
tk.Label(form_frame, text="পোস্টাল কোড:", font=("Arial", 12)).grid(row=5, column=0, sticky="e", pady=5)
entry_postal = tk.Entry(form_frame, font=("Arial", 12))
entry_postal.grid(row=5, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="দেশ:", font=("Arial", 12)).grid(row=5, column=2, sticky="e", pady=5)
entry_country = tk.Entry(form_frame, font=("Arial", 12))
entry_country.grid(row=5, column=3, pady=5, sticky="w")

# Row 6
tk.Label(form_frame, text="জাতীয় আইডি:", font=("Arial", 12)).grid(row=6, column=0, sticky="e", pady=5)
entry_nid = tk.Entry(form_frame, font=("Arial", 12))
entry_nid.grid(row=6, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="পেশা:", font=("Arial", 12)).grid(row=6, column=2, sticky="e", pady=5)
entry_occupation = tk.Entry(form_frame, font=("Arial", 12))
entry_occupation.grid(row=6, column=3, pady=5, sticky="w")

# Row 7
tk.Label(form_frame, text="কাস্টমার টাইপ:", font=("Arial", 12)).grid(row=7, column=0, sticky="e", pady=5)
customer_type_var = tk.StringVar(value='ক্রেতা')
customer_type_combo = ttk.Combobox(form_frame, textvariable=customer_type_var,
                                   values=['ক্রেতা', 'বিক্রেতা', 'ভাড়াটে', 'কিস্তি', 'অন্যান্য'], state="readonly", width=18)
customer_type_combo.grid(row=7, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="স্ট্যাটাস:", font=("Arial", 12)).grid(row=7, column=2, sticky="e", pady=5)
status_var = tk.StringVar(value='Active')
status_combo = ttk.Combobox(form_frame, textvariable=status_var,
                            values=['Active', 'Inactive'], state="readonly", width=18)
status_combo.grid(row=7, column=3, pady=5, sticky="w")

# Row 8
tk.Label(form_frame, text="নোটস:", font=("Arial", 12)).grid(row=8, column=0, sticky="ne", pady=5)
text_notes = tk.Text(form_frame, width=35, height=3, font=("Arial", 12))
text_notes.grid(row=8, column=1, pady=5, sticky="w")

# Row 9 - Add Button
btn_add = tk.Button(form_frame, text="✅ কাস্টমার যোগ করুন", bg="#4CAF50", fg="white",
                    font=("Arial", 14, "bold"), command=add_customer)
btn_add.grid(row=9, column=1, pady=15, sticky="w")

# Separator
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill=tk.X, pady=10)

# Customer List Frame
list_frame = tk.Frame(root, padx=10, pady=10)
list_frame.pack(fill=tk.BOTH, expand=True)

columns = ("আইডি", "প্রথম নাম", "শেষ নাম", "লিঙ্গ", "ফোন", "ইমেইল", "শহর", "টাইপ", "স্ট্যাটাস")
tree = ttk.Treeview(list_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

load_customers()
root.mainloop()
