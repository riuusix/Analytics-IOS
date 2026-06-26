# --- DATABASE KAPASITAS BATERAI (mAh) ---
BATTERY_DB = {
    "iPhone8,1": 1715, "iPhone8,2": 2750, "iPhone8,4": 1624, 
    "iPhone9,1": 1960, "iPhone9,3": 1960, "iPhone9,2": 2900, "iPhone9,4": 2900, 
    "iPhone10,1": 1821, "iPhone10,4": 1821, "iPhone10,2": 2691, "iPhone10,5": 2691, 
    "iPhone10,3": 2716, "iPhone10,6": 2716, 
    "iPhone11,2": 2658, "iPhone11,4": 3174, "iPhone11,6": 3174, "iPhone11,8": 2942, 
    "iPhone12,1": 3110, "iPhone12,3": 3046, "iPhone12,5": 3969, "iPhone12,8": 1821, 
    "iPhone13,1": 2227, "iPhone13,2": 2815, "iPhone13,3": 2815, "iPhone13,4": 3687, 
    "iPhone14,4": 2406, "iPhone14,5": 3227, "iPhone14,2": 3095, "iPhone14,3": 4352, "iPhone14,6": 2018, 
    "iPhone14,7": 3279, "iPhone14,8": 4325, "iPhone15,2": 3200, "iPhone15,3": 4323, 
    "iPhone15,4": 3349, "iPhone15,5": 4383, "iPhone16,1": 3274, "iPhone16,2": 4422,
    "iPhone17,1": 3561, "iPhone17,2": 4676, "iPhone17,3": 3582, "iPhone17,4": 4685, 
    # --- NEW: iPhone 17 Series (2025/2026) ---
    "iPhone18,1": 4252, # iPhone 17 Pro
    "iPhone18,2": 5088, # iPhone 17 Pro Max (Monster Battery!)
    "iPhone18,3": 3692, # iPhone 17
    "iPhone18,4": 3149,  # iPhone 17 Air (Slim) - Baterai lebih kecil karena tipis

    # --- DATA IPAD (Kapasitas Besar!) ---
    # iPad Base Model
    "iPad12,1": 8557, "iPad12,2": 8557, # iPad 9
    "iPad13,18": 7606, "iPad13,19": 7606, # iPad 10
    
    # iPad mini
    "iPad14,1": 5124, "iPad14,2": 5124, # iPad mini 6
    "iPad16,1": 5124, "iPad16,2": 5124, # iPad mini 7 (A17 Pro)

    # iPad Air
    "iPad13,1": 7606, "iPad13,2": 7606, # iPad Air 4
    "iPad13,16": 7606, "iPad13,17": 7606, # iPad Air 5 (M1)
    "iPad14,8": 7606, "iPad14,9": 7606, # iPad Air 11" (M2)
    "iPad14,10": 9800, "iPad14,11": 9800, # iPad Air 13" (M2)

    # iPad Pro 11-inch
    "iPad8,1": 7812, "iPad8,2": 7812, # Pro 11 (2018)
    "iPad8,9": 7540, "iPad8,10": 7540, # Pro 11 (2020)
    "iPad13,4": 7538, "iPad13,5": 7538, # Pro 11 (M1)
    "iPad14,3": 7538, "iPad14,4": 7538, # Pro 11 (M2)
    "iPad16,3": 8160, "iPad16,4": 8160, # Pro 11 (M4)

    # iPad Pro 12.9-inch / 13-inch
    "iPad8,5": 9720, "iPad8,6": 9720, # Pro 12.9 (Gen 3)
    "iPad8,11": 9720, "iPad8,12": 9720, # Pro 12.9 (Gen 4)
    "iPad13,8": 10758, "iPad13,9": 10758, # Pro 12.9 (M1 - Mini LED)
    "iPad14,5": 10758, "iPad14,6": 10758, # Pro 12.9 (M2)
    "iPad16,5": 10290, "iPad16,6": 10290, # Pro 13 (M4 - Tipis)
}

# --- DATABASE MODEL ---
IPHONE_MODELS = {
    "iPhone8,1": "iPhone 6s", "iPhone8,2": "iPhone 6s Plus", "iPhone8,4": "iPhone SE (1st Gen)",
    "iPhone9,1": "iPhone 7", "iPhone9,3": "iPhone 7", "iPhone9,2": "iPhone 7 Plus", "iPhone9,4": "iPhone 7 Plus",
    "iPhone10,1": "iPhone 8", "iPhone10,4": "iPhone 8", "iPhone10,2": "iPhone 8 Plus", "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X", "iPhone10,6": "iPhone X",
    "iPhone11,2": "iPhone XS", "iPhone11,4": "iPhone XS Max", "iPhone11,6": "iPhone XS Max", "iPhone11,8": "iPhone XR",
    "iPhone12,1": "iPhone 11", "iPhone12,3": "iPhone 11 Pro", "iPhone12,5": "iPhone 11 Pro Max",
    "iPhone12,8": "iPhone SE (2nd Gen)",
    "iPhone13,1": "iPhone 12 mini", "iPhone13,2": "iPhone 12", "iPhone13,3": "iPhone 12 Pro", "iPhone13,4": "iPhone 12 Pro Max",
    "iPhone14,6": "iPhone SE (3rd Gen)",
    "iPhone14,4": "iPhone 13 mini", "iPhone14,5": "iPhone 13", "iPhone14,2": "iPhone 13 Pro", "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,7": "iPhone 14", "iPhone14,8": "iPhone 14 Plus", "iPhone15,2": "iPhone 14 Pro", "iPhone15,3": "iPhone 14 Pro Max",
    "iPhone15,4": "iPhone 15", "iPhone15,5": "iPhone 15 Plus", "iPhone16,1": "iPhone 15 Pro", "iPhone16,2": "iPhone 15 Pro Max",
    "iPhone17,1": "iPhone 16 Pro", "iPhone17,2": "iPhone 16 Pro Max", "iPhone17,3": "iPhone 16", "iPhone17,4": "iPhone 16 Plus",

    # --- NEW: iPhone 17 Series (Internal ID: iPhone18,x) ---
    "iPhone18,1": "iPhone 17 Pro", 
    "iPhone18,2": "iPhone 17 Pro Max", 
    "iPhone18,3": "iPhone 17", 
    "iPhone18,4": "iPhone 17 Air", # Model tipis pengganti Plus

    # --- IPAD MODELS ---
    "iPad12,1": "iPad 9 (WiFi)", "iPad12,2": "iPad 9 (Cellular)",
    "iPad13,18": "iPad 10 (WiFi)", "iPad13,19": "iPad 10 (Cellular)",
    
    "iPad14,1": "iPad mini 6 (WiFi)", "iPad14,2": "iPad mini 6 (Cellular)",
    "iPad16,1": "iPad mini 7 (WiFi)", "iPad16,2": "iPad mini 7 (Cellular)",

    "iPad13,1": "iPad Air 4", "iPad13,2": "iPad Air 4 (Cellular)",
    "iPad13,16": "iPad Air 5 (M1)", "iPad13,17": "iPad Air 5 (M1+Cell)",
    "iPad14,8": "iPad Air 11-inch (M2)", "iPad14,9": "iPad Air 11-inch (M2+Cell)",
    "iPad14,10": "iPad Air 13-inch (M2)", "iPad14,11": "iPad Air 13-inch (M2+Cell)",

    "iPad13,4": "iPad Pro 11 (M1)", "iPad13,5": "iPad Pro 11 (M1+Cell)",
    "iPad14,3": "iPad Pro 11 (M2)", "iPad14,4": "iPad Pro 11 (M2+Cell)",
    "iPad16,3": "iPad Pro 11 (M4 - Ultra Thin)", "iPad16,4": "iPad Pro 11 (M4+Cell)",

    "iPad13,8": "iPad Pro 12.9 (M1)", "iPad13,9": "iPad Pro 12.9 (M1+Cell)",
    "iPad14,5": "iPad Pro 12.9 (M2)", "iPad14,6": "iPad Pro 12.9 (M2+Cell)",
    "iPad16,5": "iPad Pro 13 (M4 - Ultra Thin)", "iPad16,6": "iPad Pro 13 (M4+Cell)",
}

REGION_MAP = {
    "PA/A": "Indonesia (Official)", "ID/A": "Indonesia (Official)", "FE/A": "Indonesia (Official)", "SA/A": "Indonesia (Official)",
    "LL/A": "USA (International)", "ZP/A": "Singapore/HK", "ZA/A": "Singapore/Malaysia",
    "CH/A": "China (Physical Dual SIM)", "J/A": "Japan (Camera Sound Restricted)",
    "KH/A": "South Korea", "B/A": "UK/Ireland", "X/A": "Australia/NZ",
    "VN/A": "Vietnam", "MY/A": "Malaysia", "TY/A": "Italy", "FD/A": "Austria/Liechtenstein/Switzerland"
}

SENSOR_DICTIONARY = {
    "Mic1": "Microphone Bawah / Dock Charger", "Mic2": "Microphone Belakang (Kamera)", "Mic3": "Microphone Atas (FaceTime/Earpiece)",
    "PRS0": "Sensor Barometer (Dekat Tombol Power)", "TALS": "Ambient Light Sensor (Sensor Cahaya)",
    "TG0B": "Baterai (Koneksi Data)", "I2C": "Bus Jalur Data Komponen Internal",
    "NAND": "Chip Storage / Memori Internal", "Baseband": "Chip Sinyal / Modem"
}

PANIC_ADVICE_MAP = {
    "watchdog": "Analisis: Sistem restart otomatis karena komponen telat merespon. Biasanya masalah pada Baterai atau Port Charger.",
    "ans2": "Analisis: Masalah pada jalur komunikasi penyimpanan (NAND). Resiko data hilang, segera backup!",
    "sep": "Analisis: Secure Enclave Processor error. Terkait keamanan data atau Face ID/Touch ID.",
    "i2c": "Analisis: Bus komunikasi data internal konslet. Cek area Face ID atau Kamera depan.",
    "nand": "Analisis: Kerusakan chip memori internal. Hardware butuh perbaikan teknis mendalam."
}

# --- DATABASE CHIPSET / PROCESSOR ---
SOC_DB = {
    # A-Series (iPhone)
    "iPhone10,1": "A11 Bionic (10nm)", "iPhone10,2": "A11 Bionic (10nm)", "iPhone10,3": "A11 Bionic (10nm)", "iPhone10,6": "A11 Bionic (10nm)", # 8 & X
    "iPhone11,2": "A12 Bionic (7nm)", "iPhone11,6": "A12 Bionic (7nm)", "iPhone11,8": "A12 Bionic (7nm)", # XS & XR
    "iPhone12,1": "A13 Bionic (7nm+)", "iPhone12,3": "A13 Bionic (7nm+)", "iPhone12,5": "A13 Bionic (7nm+)", # 11 Series
    "iPhone12,8": "A13 Bionic (7nm+)", # SE 2
    "iPhone13,1": "A14 Bionic (5nm)", "iPhone13,2": "A14 Bionic (5nm)", "iPhone13,3": "A14 Bionic (5nm)", "iPhone13,4": "A14 Bionic (5nm)", # 12 Series
    "iPhone14,4": "A15 Bionic (5nm)", "iPhone14,5": "A15 Bionic (5nm)", "iPhone14,2": "A15 Bionic (5nm)", "iPhone14,3": "A15 Bionic (5nm)", # 13 Series
    "iPhone14,6": "A15 Bionic (5nm)", # SE 3
    "iPhone14,7": "A15 Bionic (5nm)", "iPhone14,8": "A15 Bionic (5nm)", # 14 / 14 Plus
    "iPhone15,2": "A16 Bionic (4nm)", "iPhone15,3": "A16 Bionic (4nm)", # 14 Pro
    "iPhone15,4": "A16 Bionic (4nm)", "iPhone15,5": "A16 Bionic (4nm)", # 15 / 15 Plus
    "iPhone16,1": "A17 Pro (3nm)", "iPhone16,2": "A17 Pro (3nm)", # 15 Pro
    "iPhone17,1": "A18 (3nm Gen2)", "iPhone17,2": "A18 (3nm Gen2)", "iPhone17,3": "A18 (3nm Gen2)", "iPhone17,4": "A18 (3nm Gen2)", # 16 Series
    "iPhone18,2": "A19 Pro (2nm Est)", # 17 Pro Max (Future)

    # M-Series (iPad)
    "iPad13,4": "Apple M1 (5nm)", "iPad13,5": "Apple M1 (5nm)", "iPad13,8": "Apple M1 (5nm)", "iPad13,9": "Apple M1 (5nm)", "iPad13,16": "Apple M1 (5nm)",
    "iPad14,3": "Apple M2 (5nm Gen2)", "iPad14,4": "Apple M2 (5nm Gen2)", "iPad14,5": "Apple M2 (5nm Gen2)", "iPad14,6": "Apple M2 (5nm Gen2)",
    "iPad16,3": "Apple M4 (3nm)", "iPad16,4": "Apple M4 (3nm)", "iPad16,5": "Apple M4 (3nm)", "iPad16,6": "Apple M4 (3nm)"
}
