import sqlite3

def get_connection():
    return sqlite3.connect('garage.db')

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Vehicle টেবিল
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS vehicles(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gari_nam TEXT NOT NULL,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        variant TEXT,
        color TEXT,
        baner_bochor INTEGER,
        registration_number TEXT,
        engine_number TEXT,
        chassis_number TEXT,
        fuel_type TEXT CHECK(fuel_type IN ('Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid')),
        transmission_type TEXT CHECK(transmission_type IN ('Manual', 'Automatic')),
        mileage INTEGER,
        seat_sankhya INTEGER,
        kinamulya REAL,
        bikri_mulya REAL,
        vara_dhor REAL,
        vara_masik REAL,
        kisti_mulya REAL,
        avastha TEXT CHECK(avastha IN ('Available', 'Rented', 'Sold', 'Installment')) DEFAULT 'Available',
        gari_dhoron TEXT CHECK(gari_dhoron IN ('CNG', 'Car', 'Bike', 'Truck', 'Van', 'SUV')),
        insurance_sesh DATE,
        fitness_sesh DATE,
        tax_sesh DATE,
        bibran TEXT,
        image_url TEXT,
        jog_kora_tarikh DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT CHECK(status IN ('Active', 'Inactive')) DEFAULT 'Active'
                   )
        """)
   


    # Customer টেবিল
   
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('পুরুষ', 'মহিলা', 'অন্যান্য')) DEFAULT NULL,
        date_of_birth DATE DEFAULT NULL,
        phone TEXT NOT NULL,
        email TEXT DEFAULT NULL,
        address TEXT DEFAULT NULL,
        city TEXT DEFAULT NULL,
        state TEXT DEFAULT NULL,
        postal_code TEXT DEFAULT NULL,
        country TEXT DEFAULT NULL,
        national_id TEXT DEFAULT NULL,
        occupation TEXT DEFAULT NULL,
        customer_type TEXT CHECK(customer_type IN ('ক্রেতা', 'বিক্রেতা', 'ভাড়াটে', 'কিস্তি', 'অন্যান্য')) DEFAULT 'ক্রেতা',
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        notes TEXT DEFAULT NULL,
        status TEXT CHECK(status IN ('Active', 'Inactive')) DEFAULT 'Active'
        )
    """)

    # Rental টেবিল
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            customer_id INTEGER,
            rent_date TEXT,
            return_date TEXT,
            rent_amount REAL,
            returned INTEGER DEFAULT 0,
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # Installment টেবিল
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS installments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            customer_id INTEGER,
            total_price REAL,
            paid_amount REAL DEFAULT 0,
            date TEXT,
            FOREIGN KEY(vehicle_id) REFERENCES vehicles(id),
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)

    # Installment Payment টেবিল
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS installment_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            installment_id INTEGER,
            payment_date TEXT,
            amount REAL,
            FOREIGN KEY(installment_id) REFERENCES installments(id)
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("✅ Database and tables created successfully.")
