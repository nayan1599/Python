import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime

def add_vehicle():
    gari_nam = entry_gari_nam.get().strip()
    brand = entry_brand.get().strip()
    model = entry_model.get().strip()
    variant = entry_variant.get().strip()
    color = entry_color.get().strip()
    baner_bochor = entry_baner_bochor.get().strip()
    registration_number = entry_registration_number.get().strip()
    engine_number = entry_engine_number.get().strip()
    chassis_number = entry_chassis_number.get().strip()
    fuel_type = fuel_type_var.get()
    transmission_type = transmission_var.get()
    mileage = entry_mileage.get().strip()
    seat_sankhya = entry_seat_sankhya.get().strip()
    kinamulya = entry_kinamulya.get().strip()
    bikri_mulya = entry_bikri_mulya.get().strip()
    vara_dhor = entry_vara_dhor.get().strip()
    vara_masik = entry_vara_masik.get().strip()
    kisti_mulya = entry_kisti_mulya.get().strip()
    avastha = avastha_var.get()
    gari_dhoron = gari_dhoron_var.get()
    insurance_sesh = entry_insurance_sesh.get().strip()
    fitness_sesh = entry_fitness_sesh.get().strip()
    tax_sesh = entry_tax_sesh.get().strip()
    bibran = text_bibran.get("1.0", tk.END).strip()
    image_url = entry_image_url.get().strip()
    status = status_var.get()

    if not gari_nam or not brand or not model:
        messagebox.showwarning("সতর্কতা", "গাড়ির নাম, ব্র্যান্ড এবং মডেল অবশ্যই দিতে হবে।")
        return

    # Validate year
    if baner_bochor:
        if not baner_bochor.isdigit() or not (1900 <= int(baner_bochor) <= datetime.now().year):
            messagebox.showwarning("ত্রুটি", "বানার বছর সঠিকভাবে দিন (1900 থেকে বর্তমান সাল পর্যন্ত)")
            return

    # Validate dates (insurance_sesh, fitness_sesh, tax_sesh)
    for date_str, label in [(insurance_sesh, "বিমার মেয়াদ শেষ"), (fitness_sesh, "ফিটনেস মেয়াদ শেষ"), (tax_sesh, "ট্যাক্স মেয়াদ শেষ")]:
        if date_str:
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("ত্রুটি", f"{label} তারিখ yyyy-mm-dd ফরম্যাটে দিন।")
                return

    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO vehicles (
                gari_nam, brand, model, variant, color, baner_bochor,
                registration_number, engine_number, chassis_number,
                fuel_type, transmission_type, mileage, seat_sankhya,
                kinamulya, bikri_mulya, vara_dhor, vara_masik, kisti_mulya,
                avastha, gari_dhoron, insurance_sesh, fitness_sesh, tax_sesh,
                bibran, image_url, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            gari_nam, brand, model, variant, color, int(baner_bochor) if baner_bochor else None,
            registration_number, engine_number, chassis_number,
            fuel_type, transmission_type,
            int(mileage) if mileage.isdigit() else None,
            int(seat_sankhya) if seat_sankhya.isdigit() else None,
            float(kinamulya) if kinamulya else None,
            float(bikri_mulya) if bikri_mulya else None,
            float(vara_dhor) if vara_dhor else None,
            float(vara_masik) if vara_masik else None,
            float(kisti_mulya) if kisti_mulya else None,
            avastha, gari_dhoron,
            insurance_sesh if insurance_sesh else None,
            fitness_sesh if fitness_sesh else None,
            tax_sesh if tax_sesh else None,
            bibran, image_url, status
        ))
        conn.commit()
        messagebox.showinfo("সফলতা", "গাড়ি সফলভাবে যোগ করা হয়েছে।")
        clear_form()
        load_vehicles()
    except Exception as e:
        messagebox.showerror("ত্রুটি", f"গাড়ি সংরক্ষণে সমস্যা: {e}")
    finally:
        conn.close()

def load_vehicles():
    for item in tree.get_children():
        tree.delete(item)

    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, gari_nam, brand, model, color, baner_bochor, avastha, status 
        FROM vehicles ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

def clear_form():
    entry_gari_nam.delete(0, tk.END)
    entry_brand.delete(0, tk.END)
    entry_model.delete(0, tk.END)
    entry_variant.delete(0, tk.END)
    entry_color.delete(0, tk.END)
    entry_baner_bochor.delete(0, tk.END)
    entry_registration_number.delete(0, tk.END)
    entry_engine_number.delete(0, tk.END)
    entry_chassis_number.delete(0, tk.END)
    fuel_type_var.set('Petrol')
    transmission_var.set('Manual')
    entry_mileage.delete(0, tk.END)
    entry_seat_sankhya.delete(0, tk.END)
    entry_kinamulya.delete(0, tk.END)
    entry_bikri_mulya.delete(0, tk.END)
    entry_vara_dhor.delete(0, tk.END)
    entry_vara_masik.delete(0, tk.END)
    entry_kisti_mulya.delete(0, tk.END)
    avastha_var.set('Available')
    gari_dhoron_var.set('Car')
    entry_insurance_sesh.delete(0, tk.END)
    entry_fitness_sesh.delete(0, tk.END)
    entry_tax_sesh.delete(0, tk.END)
    text_bibran.delete("1.0", tk.END)
    entry_image_url.delete(0, tk.END)
    status_var.set('Active')

root = tk.Tk()
root.title("🚗 গাড়ি ব্যবস্থাপনা")
root.geometry("1100x750")

form_frame = tk.Frame(root, padx=10, pady=10)
form_frame.pack(fill=tk.X)

# Row 0
tk.Label(form_frame, text="গাড়ির নাম:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
entry_gari_nam = tk.Entry(form_frame, font=("Arial", 12))
entry_gari_nam.grid(row=0, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ব্র্যান্ড:", font=("Arial", 12)).grid(row=0, column=2, sticky="e", pady=5)
entry_brand = tk.Entry(form_frame, font=("Arial", 12))
entry_brand.grid(row=0, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="মডেল:", font=("Arial", 12)).grid(row=0, column=4, sticky="e", pady=5)
entry_model = tk.Entry(form_frame, font=("Arial", 12))
entry_model.grid(row=0, column=5, pady=5, sticky="w")

# Row 1
tk.Label(form_frame, text="ভ্যারিয়েন্ট:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
entry_variant = tk.Entry(form_frame, font=("Arial", 12))
entry_variant.grid(row=1, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="রং:", font=("Arial", 12)).grid(row=1, column=2, sticky="e", pady=5)
entry_color = tk.Entry(form_frame, font=("Arial", 12))
entry_color.grid(row=1, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="বানার বছর:", font=("Arial", 12)).grid(row=1, column=4, sticky="e", pady=5)
entry_baner_bochor = tk.Entry(form_frame, font=("Arial", 12))
entry_baner_bochor.grid(row=1, column=5, pady=5, sticky="w")

# Row 2
tk.Label(form_frame, text="রেজিস্ট্রেশন নম্বর:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
entry_registration_number = tk.Entry(form_frame, font=("Arial", 12))
entry_registration_number.grid(row=2, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ইঞ্জিন নম্বর:", font=("Arial", 12)).grid(row=2, column=2, sticky="e", pady=5)
entry_engine_number = tk.Entry(form_frame, font=("Arial", 12))
entry_engine_number.grid(row=2, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="চ্যাসিস নম্বর:", font=("Arial", 12)).grid(row=2, column=4, sticky="e", pady=5)
entry_chassis_number = tk.Entry(form_frame, font=("Arial", 12))
entry_chassis_number.grid(row=2, column=5, pady=5, sticky="w")

# Row 3
tk.Label(form_frame, text="জ্বালানীর ধরন:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5)
fuel_type_var = tk.StringVar(value='Petrol')
fuel_type_combo = ttk.Combobox(form_frame, textvariable=fuel_type_var, values=['Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid'], state="readonly", width=15)
fuel_type_combo.grid(row=3, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ট্রান্সমিশন ধরন:", font=("Arial", 12)).grid(row=3, column=2, sticky="e", pady=5)
transmission_var = tk.StringVar(value='Manual')
transmission_combo = ttk.Combobox(form_frame, textvariable=transmission_var, values=['Manual', 'Automatic'], state="readonly", width=15)
transmission_combo.grid(row=3, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="মাইলেজ:", font=("Arial", 12)).grid(row=3, column=4, sticky="e", pady=5)
entry_mileage = tk.Entry(form_frame, font=("Arial", 12))
entry_mileage.grid(row=3, column=5, pady=5, sticky="w")

# Row 4
tk.Label(form_frame, text="সিট সংখ্যা:", font=("Arial", 12)).grid(row=4, column=0, sticky="e", pady=5)
entry_seat_sankhya = tk.Entry(form_frame, font=("Arial", 12))
entry_seat_sankhya.grid(row=4, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="কিনামূল্য:", font=("Arial", 12)).grid(row=4, column=2, sticky="e", pady=5)
entry_kinamulya = tk.Entry(form_frame, font=("Arial", 12))
entry_kinamulya.grid(row=4, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="বিক্রয় মূল্য:", font=("Arial", 12)).grid(row=4, column=4, sticky="e", pady=5)
entry_bikri_mulya = tk.Entry(form_frame, font=("Arial", 12))
entry_bikri_mulya.grid(row=4, column=5, pady=5, sticky="w")

# Row 5
tk.Label(form_frame, text="ভাড়া ধর:", font=("Arial", 12)).grid(row=5, column=0, sticky="e", pady=5)
entry_vara_dhor = tk.Entry(form_frame, font=("Arial", 12))
entry_vara_dhor.grid(row=5, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ভাড়া মাসিক:", font=("Arial", 12)).grid(row=5, column=2, sticky="e", pady=5)
entry_vara_masik = tk.Entry(form_frame, font=("Arial", 12))
entry_vara_masik.grid(row=5, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="কিস্তি মূল্য:", font=("Arial", 12)).grid(row=5, column=4, sticky="e", pady=5)
entry_kisti_mulya = tk.Entry(form_frame, font=("Arial", 12))
entry_kisti_mulya.grid(row=5, column=5, pady=5, sticky="w")

# Row 6
tk.Label(form_frame, text="অবস্থা:", font=("Arial", 12)).grid(row=6, column=0, sticky="e", pady=5)
avastha_var = tk.StringVar(value='Available')
avastha_combo = ttk.Combobox(form_frame, textvariable=avastha_var, values=['Available', 'Rented', 'Sold', 'Installment'], state="readonly", width=15)
avastha_combo.grid(row=6, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="গাড়ির ধরন:", font=("Arial", 12)).grid(row=6, column=2, sticky="e", pady=5)
gari_dhoron_var = tk.StringVar(value='Car')
gari_dhoron_combo = ttk.Combobox(form_frame, textvariable=gari_dhoron_var, values=['CNG', 'Car', 'Bike', 'Truck', 'Van', 'SUV'], state="readonly", width=15)
gari_dhoron_combo.grid(row=6, column=3, pady=5, sticky="w")

# Row 7
tk.Label(form_frame, text="বিমা শেষ:", font=("Arial", 12)).grid(row=7, column=0, sticky="e", pady=5)
entry_insurance_sesh = tk.Entry(form_frame, font=("Arial", 12))
entry_insurance_sesh.grid(row=7, column=1, pady=5, sticky="w")

tk.Label(form_frame, text="ফিটনেস শেষ:", font=("Arial", 12)).grid(row=7, column=2, sticky="e", pady=5)
entry_fitness_sesh = tk.Entry(form_frame, font=("Arial", 12))
entry_fitness_sesh.grid(row=7, column=3, pady=5, sticky="w")

tk.Label(form_frame, text="ট্যাক্স শেষ:", font=("Arial", 12)).grid(row=7, column=4, sticky="e", pady=5)
entry_tax_sesh = tk.Entry(form_frame, font=("Arial", 12))
entry_tax_sesh.grid(row=7, column=5, pady=5, sticky="w")

# Row 8
tk.Label(form_frame, text="বিবরণ:", font=("Arial", 12)).grid(row=8, column=0, sticky="ne", pady=5)
text_bibran = tk.Text(form_frame, width=60, height=4, font=("Arial", 12))
text_bibran.grid(row=8, column=1, columnspan=5, pady=5, sticky="w")

# Row 9
tk.Label(form_frame, text="ছবির URL:", font=("Arial", 12)).grid(row=9, column=0, sticky="e", pady=5)
entry_image_url = tk.Entry(form_frame, font=("Arial", 12), width=60)
entry_image_url.grid(row=9, column=1, columnspan=5, pady=5, sticky="w")

# ... আপনার অন্য GUI এলিমেন্টের নিচে (যেমন row=10)
tk.Label(form_frame, text="স্ট্যাটাস:", font=("Arial", 12)).grid(row=10, column=0, sticky="e", pady=5)
status_var = tk.StringVar(value='Active')
status_combo = ttk.Combobox(form_frame, textvariable=status_var, values=['Active', 'Inactive'], state="readonly", width=15)
status_combo.grid(row=10, column=1, pady=5, sticky="w")


# Add Button
btn_add = tk.Button(form_frame, text="গাড়ি যোগ করুন", bg="#4CAF50", fg="white",
                    font=("Arial",14,"bold"), command=add_vehicle)
btn_add.grid(row=10, column=1, pady=15, sticky="w")

# List Frame
list_frame = tk.Frame(root, padx=10, pady=10)
list_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "গাড়ির নাম", "ব্র্যান্ড", "মডেল", "রং", "বানার বছর", "অবস্থা", "স্ট্যাটাস")
tree = ttk.Treeview(list_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill=tk.BOTH, expand=True)

load_vehicles()

root.mainloop()
