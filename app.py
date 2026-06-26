import re
from flask import Flask, render_template, request, jsonify
# Menggunakan SDK Terbaru
from google import genai


app = Flask(__name__)

# --- KONFIGURASI AI ---
# Ganti dengan API Key kamu yang baru jika sudah ada
client = genai.Client(api_key="--------")

def get_ai_expert_analysis(content):
    prompt = f"""
    Kamu adalah Senior Hardware Engineer di Apple Service Center. 
    Analisis data log iPhone berikut ini secara mendalam.
    
    Data Log:
    {content[:2000]} 

    Tugasmu:
    1. Jika ini log Panic (bug_type 210), cari penyebab utama crash (Panic String).
    2. Identifikasi komponen hardware yang rusak (misal: Mic1, I2C, NAND, Voltage, dll).
    3. Berikan 3 langkah solusi teknis yang jelas dan actionable.
    
    Gunakan bahasa Indonesia yang santai tapi profesional.
    Jangan gunakan format markdown bold/italic yang berlebihan, cukup teks poin-poin.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        return [response.text]
    except Exception as e:
        return "AI Analysis unavailable."


# --- DATABASE SPEK TEKNIS LAINNYA ---
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
# --- LOGIKA KONEKTIVITAS & FITUR ---
def get_connectivity_info(wifi_code, baseband_code, model_name):
    # 1. Translate WiFi Chipset
    wifi_desc = "Unknown WiFi"
    if "4355" in wifi_code: wifi_desc = "WiFi 5 (802.11ac)"
    elif "4361" in wifi_code: wifi_desc = "WiFi 6 (802.11ax)" # iPhone 11
    elif "4378" in wifi_code: wifi_desc = "WiFi 6 (802.11ax)" # iPhone 12/13/14
    elif "4387" in wifi_code: wifi_desc = "WiFi 6E (6GHz Ready)" # iPhone 15 Pro
    elif "4399" in wifi_code: wifi_desc = "WiFi 7 (Ultra Fast)" # iPhone 16
    elif "4401" in wifi_code: wifi_desc = "WiFi 7 (iPad M4)" 
    else: wifi_desc = f"Chip ID: {wifi_code}" # Fallback
    
    # 2. Translate Modem (Baseband)
    modem_desc = "LTE / 4G"
    if "mav" in baseband_code.lower():
        # Kasarannya aja, kode mav biasanya Qualcomm 5G
        modem_desc = "5G (Qualcomm Snapdragon)"
    elif "intel" in baseband_code.lower():
        modem_desc = "LTE (Intel Modem)"
        
    # 3. Deteksi Layar (Logic Sederhana dari Nama Model)
    screen_desc = "OLED 60Hz"
    if "Pro" in model_name: # Pro & Pro Max biasanya 120Hz
        screen_desc = "OLED 120Hz (ProMotion)"
    elif "LCD" in model_name or "11" in model_name or "XR" in model_name: 
        if "Pro" not in model_name: screen_desc = "IPS LCD 60Hz" # iPhone 11 / XR
        
    return wifi_desc, modem_desc, screen_desc

# --- LOGIKA DIAGNOSA MANUAL ---
def analyze_diagnostics(content, raw_data):
    insights = []
    
    # 1. Analisis Baterai
    try:
        health = int(raw_data.get("battery_health", 100)) if raw_data.get("battery_health") != "N/A" else 100
        cycles = int(raw_data.get("cycle_count", 0)) if raw_data.get("cycle_count") != "N/A" else 0
        
        # Logic Normal (Service)
        if health < 80 and health > 0: 
            insights.append("❌ Baterai: Status Service (Kesehatan < 80%). Segera lakukan penggantian.")
        
        # Logic Anomali (Pilihan Opsi 2: Lebih Halus & Informatif)
        elif cycles > 1000 and health > 90:
            insights.append("⚠️ PERHATIAN: Statistik baterai terlihat tidak wajar (Anomali).")
            insights.append(f"Analisis: Dengan pemakaian {cycles} siklus, secara teori kimia baterai kesehatan harusnya sudah menurun (biasanya <80%).") 
            insights.append(f"Saran: Angka {health}% ini perlu diverifikasi ulang lewat durasi pemakaian nyata.")

        # Logic High Cycle tapi Health Wajar
        elif cycles > 800 and health <= 90: 
            insights.append("⚠️ Baterai: Siklus sangat tinggi, performa drop adalah hal yang wajar.")
            
    except: pass

    # 2. Analisis Kernel Panic
    if "panicString" in content:
        insights.append("🚨 CRASH FATAL: Terdeteksi Kernel Panic (Logika Mesin Error)")
        if "NAND" in content: insights.append("❌ MEMORY: Ada indikasi kegagalan chip NAND Storage.")
        missing = re.search(r"Missing sensor\(s\):\s*([^\n\r]+)", content)
        if missing:
            codes = missing.group(1).split()
            for c in codes:
                readable = SENSOR_DICTIONARY.get(c, f"Komponen Internal ({c})")
                insights.append(f"❌ SENSOR: {readable} tidak terdeteksi (Putus/Rusak)")

    # 3. Analisis Sinyal
    if "baseband_crash" in content.lower() or "bb_panic" in content.lower():
        insights.append("❌ SINYAL: Terdeteksi masalah pada modem baseband.")

    # 4. Analisis Suhu (Logic Fixed: Dibagi 10 jika > 100)
    if raw_data.get("peak_temp") != "N/A":
        try:
            raw_temp = float(raw_data["peak_temp"])
            real_temp = raw_temp / 10 if raw_temp > 100 else raw_temp
            if real_temp > 45:
                insights.append(f"🔥 THERMAL: HP pernah mencapai suhu ekstrem ({real_temp}°C).")
        except: pass

    return insights if insights else ["✅ Semua sistem hardware terdeteksi normal."]

# --- LOGIKA DIAGNOSA PANIC (RULE BASED) ---
def get_panic_expert_advice(content):
    advice = []
    missing_match = re.search(r"Missing sensor\(s\):\s*([^\n\r]+)", content)
    if missing_match:
        codes = missing_match.group(1).split()
        for c in codes:
            if c == "Mic1": advice.append("Saran: Bersihkan atau ganti Flex Port Charger (Mic1 rusak).")
            if c == "PRS0": advice.append("Saran: Cek fleksibel tombol Power/Volume (Sensor Barometer PRS0).")
            if c == "TALS": advice.append("Saran: Cek area sensor cahaya di layar atas (Face ID terganggu).")
            if c == "TG0B": advice.append("Saran: Ganti Baterai. Jalur data TG0B tidak terbaca.")

    content_lower = content.lower()
    for key, text in PANIC_ADVICE_MAP.items():
        if key in content_lower:
            advice.append(text)

    return advice if advice else ["Saran: Lakukan Restore via iTunes. Jika tetap restart, ada masalah jalur di Motherboard."]

# --- PARSER UTAMA ---
def parse_ips_data(content):
    # # --- PASANG CCTV DISINI (HAPUS NANTI KALAU UDAH FIX) ---
    print("\n" + "="*50 + " ISI FILE LOG (HEADER) " + "="*50)
    print(content[:1000]) # Kita intip 1000 karakter pertama
    print("="*120 + "\n")
    # # -------------------------------------------------------
    # 1. Deteksi Tipe Log
    is_panic = "panicString" in content or '"bug_type":210' in content or '"bug_type":"210"' in content
    
# 2. Identifikasi Hardware (LOGIC HYBRID IPHONE & IPAD)
    hw_code = "N/A"
    
    # LEVEL 1: Cari ID Eksplisit (Universal Regex)
    # Regex ini baca: "Cari kata iPhone ATAU iPad, diikuti angka, koma, angka"
    hw_matches = re.findall(r'((?:iPhone|iPad)\d+,\d+)', content)
    
    if hw_matches:
        hw_code = hw_matches[0]
        print(f"DEBUG: Identitas ditemukan via ID -> {hw_code}")

    # LEVEL 2: Forensik Chipset (KHUSUS IPHONE SAJA)
    # Kita kasih pagar "if 'iPad' not in hw_code" biar logika detektif iPhone gak ngerusak data iPad
    elif "iPad" not in hw_code: 
        print("DEBUG: ID tidak ditemukan, memulai analisis WiFi & Baseband (iPhone Logic)...")        
        # Ambil data chipset & RAM
        bb_match = re.search(r'"basebandChipset"\s*:\s*"([^"]+)"', content)
        wifi_match = re.search(r'"WiFiChipset"\s*:\s*"([^"]+)"', content)
        ram_match = re.search(r'"dramSize"\s*:\s*([\d\.]+)', content)
        
        bb_val = bb_match.group(1) if bb_match else ""
        wifi_val = wifi_match.group(1) if wifi_match else ""
        ram_val = float(ram_match.group(1)) if ram_match else 0
        
        # --- LOGIC DETEKTIF WIFI (SEMUA IPHONE PUNYA KODE UNIK) ---
        
        # KELOMPOK 1: IPHONE 12 / 13 / 14 / SE3 (WiFi 4387)
        if "4387" in wifi_val:
            # Perbaikan: Jangan pakai RAM untuk bedain 12 vs 13 (karena sama-sama 4GB)
            # Wajib pakai kode Modem (Baseband)
            
            if "mav21" in bb_val: # Khas iPhone 13 Series
                if ram_val > 5.0: hw_code = "iPhone14,2" # 13 Pro (6GB)
                else: hw_code = "iPhone14,5" # 13 Biasa (4GB)
                
            elif "mav20" in bb_val: # Khas iPhone 12 Series
                if ram_val > 5.0: hw_code = "iPhone13,3" # 12 Pro (6GB)
                else: hw_code = "iPhone13,2" # 12 Biasa (4GB)
                
            # Fallback (Kalau baseband aneh/kosong, baru tebak RAM)
            else:
                 if ram_val > 3.4: hw_code = "iPhone14,5" # Asumsi ke 13 aja biar aman

        # KELOMPOK 2: IPHONE 11 SERIES (WiFi 4378)
        elif "4378" in wifi_val:
            if ram_val > 3.5: hw_code = "iPhone12,1" # iPhone 11
            
        # KELOMPOK 3: IPHONE XR / XS (WiFi 4377)
        elif "4377" in wifi_val:
            if ram_val < 3.5:
                hw_code = "iPhone11,8" # iPhone XR (RAM 3GB)
            else:
                hw_code = "iPhone11,2" # iPhone XS (RAM 4GB)

        # KELOMPOK 4: IPHONE X / 8 PLUS (WiFi 4357) -> KASUS TEMANMU
        elif "4357" in wifi_val:
            # Kita panggil detektif bantuan: Cek OS & Kapasitas Baterai
            
            # Ambil data pembantu
            raw_cap_str = re.search(r'"last_value_AppleRawMaxCapacity":\s*(\d+)', content)
            raw_cap = int(raw_cap_str.group(1)) if raw_cap_str else 0
            
            os_ver = re.search(r'"os_version"\s*:\s*"([^"]+)"', content)
            os_str = os_ver.group(1) if os_ver else ""
            
            print(f"DEBUG KONFLIK: WiFi 4357 terdeteksi. Cek OS: {os_str} | Bat: {raw_cap}")

            # LOGIKA JURI HAKIM:
            # 1. Kalau iOS 17 atau 18 ke atas -> PASTI XR (X/8 mentok di iOS 16)
            if "iPhone OS 17" in os_str or "iPhone OS 18" in os_str:
                hw_code = "iPhone11,8" # Vonis: iPhone XR
                print("DEBUG: Fix XR karena pakai iOS 17/18")
                
            # 2. Kalau Baterai aslinya > 2900 mAh -> PASTI XR (X cuma 2700an)
            elif raw_cap > 2900:
                hw_code = "iPhone11,8" # Vonis: iPhone XR
                print("DEBUG: Fix XR karena kapasitas baterai badak")
                
            # 3. Kalau tidak keduanya, baru kita anggap X atau 8 Plus
            else:
                if ram_val > 2.5: 
                    detected_model_name = "iPhone X / 8 Plus (A11 Bionic)"
                    hw_code = "CUSTOM_X_8P"
                else:
                    hw_code = "iPhone10,1" # iPhone 8 Biasa

    # 3. Ekstraksi Data (Regex Standar)
    patterns = {
        "os_version": r'"os_version"\s*:\s*"([^"]+)"',
        "sku": r'"productSku"\s*:\s*"([^"]+)"',
        "capacity": r'"deviceCapacity"\s*:\s*(\d+)',
        "ram": r'"dramSize"\s*:\s*([\d\.]+)',
        "carrier": r'"homeCarrierName"\s*:\s*"([^"]+)"',
        "baseband": r'"basebandFirmwareVersion"\s*:\s*"([^"]+)"',
        "wifi_chip": r'"WiFiChipset"\s*:\s*"([^"]+)"',         
        "battery_health": r'"last_value_MaximumCapacityPercent":\s*(\d+)',
        "cycle_count": r'"last_value_CycleCount":\s*(\d+)',
        "peak_temp": r'"last_value_MaximumTemperature":\s*(\d+)',
        "raw_capacity": r'"last_value_AppleRawMaxCapacity":\s*(\d+)', 
        "uptime": r'"uptime"\s*:\s*(\d+)',
        "nand_key_1": r'"f_NandWrittenBytes"\s*:\s*(\d+)',      # Paling umum
        "nand_key_2": r'"cells_nand_writes"\s*:\s*(\d+)',       # iOS versi transisi
        "nand_key_3": r'"NandWrites"\s*:\s*(\d+)',              # Versi iPad kadang gini
        "nand_key_4": r'"TotalNandWrites"\s*:\s*(\d+)',         # Versi Developer
        "nand_key_5": r'"data_written"\s*:\s*(\d+)',            # Versi Lawas banget
        "build_id": r'OS\s+[\d\.]+\s+\(([^)]+)\)', 
        "panic_process": r'process\s*:\s*([\w\d\.]+)',
        "top_cat_1": r'"TopCategory1"\s*:\s*"([^"]+)"',
        "top_cat_2": r'"TopCategory2"\s*:\s*"([^"]+)"',
        "high_eng_1": r'"HighEngagementCategory1"\s*:\s*"([^"]+)"',
    }    
    
    res = {k: (re.search(v, content).group(1) if re.search(v, content) else "N/A") for k, v in patterns.items()}

    # 4. Logika UI Mode (Adaptif)
    is_battery_data_present = res["battery_health"] != "N/A"

    if is_panic and not is_battery_data_present:
        res["ui_mode"] = "PANIC_FULL_ONLY" 
    elif is_panic and is_battery_data_present:
        res["ui_mode"] = "ANALYTIC_WITH_ERROR" 
    else:
        res["ui_mode"] = "NORMAL_ANALYTIC" 

# 5. Mapping Model & Region
    if hw_code != "N/A" and hw_code in IPHONE_MODELS:
        res["model_name"] = IPHONE_MODELS[hw_code]
        design_cap = BATTERY_DB.get(hw_code, 0)
        res["design_capacity"] = f"{design_cap} mAh" if design_cap > 0 else "N/A"
        
    else:
        # Fallback Logic (Kalo ID ketemu tapi gak ada di DB, atau ID gak ketemu)
        if "iPad" in hw_code:
            res["model_name"] = f"iPad Unknown Model ({hw_code})"
            res["design_capacity"] = "Cek Database Manual"
        else:
            # Masuk ke Skenario B (Tebakan RAM iPhone) yang lama
            res["design_capacity"] = "Estimasi: 2400-3200 mAh"
        try:
            # Konversi RAM ke angka desimal
            ram_val = float(res.get("ram", "0"))
            
            if 1.8 <= ram_val <= 2.2:
                res["model_name"] = "iPhone 6s/7/8/SE (2GB RAM)"
            elif 2.7 <= ram_val <= 3.3:
                res["model_name"] = "iPhone X/XR/8 Plus (3GB RAM)"
                res["design_capacity"] = "± 2700-2900 mAh"
            elif 3.6 <= ram_val <= 4.3: 
                # Range iPhone 11/12/13 non-Pro
                res["model_name"] = "iPhone 11 / 12 / 13 Series (4GB RAM)"
                res["design_capacity"] = "Cek Pengaturan HP"
            elif 5.6 <= ram_val <= 6.4:
                res["model_name"] = "iPhone 12/13/14 Pro Series (6GB RAM)"
            elif ram_val > 7.5:
                res["model_name"] = "iPhone 15 Pro / 16 Series (8GB RAM)"
            else:
                res["model_name"] = f"iPhone Tidak Dikenal (RAM {ram_val}GB)"
                
        except:
            res["model_name"] = f"iPhone Unknown ({hw_code})"

    # Ambil Actual Capacity (Kalo ada di log, TAMPILKAN!)
    # Logika: Kalau raw_capacity ada isinya, kita format jadi mAh. 
    res["actual_capacity"] = f"{res['raw_capacity']} mAh" if res.get('raw_capacity') and res['raw_capacity'] != "N/A" else "N/A"

    res["region_name"] = REGION_MAP.get(res["sku"], f"Global ({res['sku']})")
    # 6. Hybrid Intelligence (AI + Manual)
    if is_panic:
        res["expert_advice"] = get_ai_expert_analysis(content)
        panic_match = re.search(r'panicString"\s*:\s*"([^"]+)"', content)
        res["panic_snippet"] = panic_match.group(1)[:300] if panic_match else "Detail panic tidak ditemukan."
        res["diagnostics"] = ["🚨 AI SEDANG MENGANALISIS CRASH..."]
        manual_diag = analyze_diagnostics(content, res)
        if manual_diag: res["diagnostics"].extend(manual_diag)
    else:
        res["expert_advice"] = ["Sistem Normal. Gunakan log Panic untuk analisa hardware."]
        res["panic_snippet"] = ""
        res["diagnostics"] = analyze_diagnostics(content, res)

    # 7. Formatting Angka & Hitung Real Health
    # --- [FIX BUG SUHU] ---
    if res.get("peak_temp") and res["peak_temp"] != "N/A":
        try:
            temp_val = float(res["peak_temp"])
            # Logic: Jika angkanya ratusan (misal 483), berarti harus dibagi 10 jadi 48.3
            # Karena gak mungkin iPhone idup di suhu 100 derajat celcius wkwk
            if temp_val > 100:
                temp_val = temp_val / 10
            
            res["peak_temp"] = f"{temp_val}"
        except:
            res["peak_temp"] = "N/A"

    # --- STEP 8 : CONNECTIVITY & SCREEN INFO ---
    # --- FITUR: CONNECTIVITY TRANSLATOR & SCREEN ---
    wifi_clean, modem_clean, screen_clean = get_connectivity_info(
        res.get("wifi_chip", ""), 
        res.get("baseband", ""), 
        res.get("model_name", "")
    )
    
    res["wifi_desc"] = wifi_clean
    res["modem_desc"] = modem_clean
    res["screen_desc"] = screen_clean

    # --- FITUR: STORAGE HEALTH (NAND WEAR) ---
    res["storage_wear"] = "N/A"
    res["storage_tbw"] = "0"
    
    # Gabungin hasil regex (karena key-nya suka beda-beda tiap iOS)
# [UPDATE STEP 7: GABUNGKAN SEMUA JARING]
    # Cek satu-satu, siapa tau nyangkut di salah satu key
    nand_bytes = "N/A"
    
    # List prioritas pengecekan
    keys_to_check = ["nand_key_1", "nand_key_2", "nand_key_3", "nand_key_4", "nand_key_5"]
    
    for key in keys_to_check:
        if res.get(key) and res.get(key) != "N/A":
            nand_bytes = res[key]
            break # Udah ketemu, stop nyari
    
    # Lanjut ke logika konversi TB kayak kemarin...
    res["storage_wear"] = "N/A"
    res["storage_tbw"] = "0"
    
    if nand_bytes != "N/A":
        # ... (Copy logic konversi TB yang kemarin disini) ...
        try:
            bytes_val = float(nand_bytes)
            # Konversi ke Terabyte (TB)
            # Rumus: Bytes -> KB -> MB -> GB -> TB (bagi 1024^4)
            tbw = bytes_val / (1024**4) 
            
            # Formatting
            if tbw < 1:
                # Kalau masih kecil, pake GB
                gbw = bytes_val / (1024**3)
                res["storage_tbw"] = f"{gbw:.1f} GB"
                res["storage_wear"] = "Sangat Sehat (Low Usage)"
            else:
                res["storage_tbw"] = f"{tbw:.2f} TB"
                
                # Analisa Kesehatan Storage (Asumsi kasar umur NAND iPhone)
                if tbw > 150: res["storage_wear"] = "⚠️ Critical (Memory Worn Out)"
                elif tbw > 75: res["storage_wear"] = "Heavy Usage (SSD Lelah)"
                elif tbw > 25: res["storage_wear"] = "Normal Usage"
                else: res["storage_wear"] = "Sehat (Low Usage)"   
        except: pass

    # --- FITUR: SMART CARRIER & IMEI CHECK (REVISI CERDAS) ---  
    # 1. Bersihkan Nama Carrier
    invalid_carriers = ["N/A", "unknown", "<unknown>", "null", ""]
    has_signal = True # Asumsi awal ada sinyal
    
    if res["carrier"] in invalid_carriers:
        has_signal = False
        if "iPad" in res["model_name"] and "Cellular" not in res["model_name"]:
            res["carrier"] = "WiFi Only"
        else:
            res["carrier"] = "No Signal"

    # 2. Detektif Region (Ex-Inter vs Resmi Indo)
    indo_regions = ["PA/A", "ID/A", "FE/A", "SA/A"]
    current_region = res.get("sku", "")
    is_indo_unit = any(x in current_region for x in indo_regions)
    
    # 3. Logika Analisa (Cek Status Kemenperin secara tidak langsung)
    if "iPhone" in res["model_name"]:
        if not is_indo_unit: 
            # KASUS UNIT EX-INTER (LL/A, ZP/A, dll)
            if has_signal:
                # Ada sinyal operator (misal Telkomsel) -> Berarti Terdaftar/Whitelisted
                res["carrier"] += " (Ex-Inter ✅)"
            else:
                # Gak ada sinyal -> Curiga Blokir ATAU No SIM
                res["carrier"] += " ⚠️"
                if "diagnostics" in res:
                    res["diagnostics"].append("⚠️ SINYAL: Unit Ex-Inter (LL/A) hilang sinyal. Pastikan IMEI terdaftar atau Kartu SIM terpasang.")
        
        elif is_indo_unit and not has_signal:
            # KASUS UNIT RESMI INDO (PA/A) TAPI GAK ADA SINYAL
            # Ini biasanya cuma masalah kartu/IC Baseband, bukan blokir.
            res["carrier"] += " (Cek SIM)"
            
    # --- [FITUR REAL HEALTH (YANG UDAH ADA)] ---
    if res.get("raw_capacity") and res["raw_capacity"] != "N/A":
        try:
            design_cap_clean = res["design_capacity"].replace(" mAh", "").replace("Estimasi: ", "").split("-")[0].strip()
            
            if design_cap_clean.isdigit():
                design_cap_val = int(design_cap_clean)
                raw_cap_val = int(res["raw_capacity"])
                
                real_health_pct = (raw_cap_val / design_cap_val) * 100
                res["real_health_calculated"] = f"{real_health_pct:.1f}%"
        except:
            res["real_health_calculated"] = "N/A"
    
    # 9. Deteksi Logic Uptime & Age    
    # 1. LOGIC UPTIME (FORENSIK)
    res["uptime_desc"] = "N/A"
    if res.get("uptime") and res["uptime"] != "N/A":
        try:
            ms = int(res["uptime"])
            seconds = ms / 1000
            
            if seconds < 60:
                res["uptime_desc"] = f"CRITICAL: {int(seconds)} Detik (Bootloop!)"
            elif seconds < 3600:
                res["uptime_desc"] = f"{int(seconds/60)} Menit (Unstable)"
            elif seconds < 86400:
                res["uptime_desc"] = f"{int(seconds/3600)} Jam (Random Crash)"
            else:
                res["uptime_desc"] = f"{int(seconds/86400)} Hari (Long Uptime)"
        except: pass

    # [UPDATE STEP 7: USER PERSONA / HABIT]
    
    # Ambil datanya
    cat1 = res.get("top_cat_1", "N/A")
    cat2 = res.get("top_cat_2", "N/A")
    eng1 = res.get("high_eng_1", "N/A")
    
    # Gabungin jadi satu list biar gampang dicek
    habits = [cat1, cat2, eng1]
    habits_str = " ".join(habits).lower()
    
    # LOGIKA TEBAK-TEBAKAN KEPRIBADIAN
    res["user_persona"] = "Unknown User"
    res["persona_icon"] = "👤"
    res["persona_desc"] = "Pola pemakaian tidak terdeteksi spesifik."
    
    if "games" in habits_str:
        res["user_persona"] = "GAMER SEJATI"
        res["persona_icon"] = "🎮"
        res["persona_desc"] = "Dominasi aplikasi Game. Cek responsivitas layar & suhu."
        
    elif "social" in habits_str or "entertainment" in habits_str:
        res["user_persona"] = "SOCIAL BUTTERFLY"
        res["persona_icon"] = "📱"
        res["persona_desc"] = "Aktif di Sosmed/Entertainment. Cek kesehatan layar (burn-in) & kamera."
        
    elif "productivity" in habits_str or "utilities" in habits_str or "finance" in habits_str:
        res["user_persona"] = "PRODUCTIVE WORKER"
        res["persona_icon"] = "💼"
        res["persona_desc"] = "Device dipakai kerja/utilitas. Biasanya kondisi fisik lebih terawat."
        
    elif "photo" in habits_str or "video" in habits_str:
        res["user_persona"] = "CONTENT CREATOR"
        res["persona_icon"] = "📸"
        res["persona_desc"] = "Fokus di Foto/Video. Cek detail lensa kamera & stabilizer."
    # --- FITUR BARU: OS QUALITY CHECK (BETA DETECTOR) ---
    res["os_quality"] = "Official Release ✅"
    res["os_badge_color"] = "bg-green-100 text-green-700"
    
    if res.get("build_id") != "N/A":
        build_id = res["build_id"]
        # Logika: Build number Beta biasanya diakhiri huruf (a, b, e, f, dll)
        # Contoh Stable: 21A329
        # Contoh Beta: 21A5329e
        if build_id[-1].isalpha(): 
            res["os_quality"] = "BETA / TEST VERSION ⚠️"
            res["os_badge_color"] = "bg-yellow-100 text-yellow-700"
            res["diagnostics"].append("⚠️ SYSTEM: Menggunakan iOS Beta. Wajar jika panas/buggy.")

    # --- FITUR BARU: THE CULPRIT (TERSANGKA CRASH) ---
    res["crash_culprit"] = "-"
    if is_panic:
        # Coba cari nama proses di regex
        proc = re.search(r'process\s*:\s*([\w\d\.]+)', content)
        if proc:
            culprit = proc.group(1)
            res["crash_culprit"] = culprit
            
            # Analisa Sederhana
            if "kernel" in culprit:
                res["diagnostics"].append("🚨 CRASH SOURCE: Kernel (Mesin/OS). Indikasi Hardware Failure.")
            elif "SpringBoard" in culprit or "backboardd" in culprit:
                res["diagnostics"].append("📱 CRASH SOURCE: UI System (Software/Bug iOS). Bukan Hardware.")
            else:
                res["diagnostics"].append(f"📱 CRASH SOURCE: Aplikasi '{culprit}'. Coba uninstall aplikasi ini.")

    # --- [INTEGRATED PROFILING SYSTEM: BEHAVIOR + AGE + USAGE] ---
    # Default Values
    res["user_behavior"] = "🔍 ANALYZING..."
    res["behavior_desc"] = "Data tidak cukup."
    res["behavior_color"] = "text-gray-500"
    res["age_estimation"] = "Menunggu Data..."
    
    # Kita butuh Cycle & Real Health buat kalkulasi ini
    if res.get("cycle_count") != "N/A" and res.get("cycle_count").isdigit():
        try:
            cycles = int(res["cycle_count"])
            
            # 1. Tentukan Real Health (Kalau gak ada, pake Health biasa)
            if res.get("real_health_calculated") != "N/A":
                curr_health = float(str(res["real_health_calculated"]).replace("%", ""))
            else:
                curr_health = float(res.get("battery_health", "100"))
                
            # 2. Hitung Degradasi per Cycle (Seberapa parah rusaknya per 1x cas)
            lost_health = 100 - curr_health
            
            # Cegah division by zero
            degrade_rate = lost_health / cycles if cycles > 0 else 0
            
            # 3. TENTUKAN FAKTOR PENGALI (Daily Charging Frequency)
            # Semakin tinggi degrade rate -> Asumsi semakin sering ngecas (panas/main game)
            daily_factor = 1.0 # Default (1 cycle = 1 hari)
            
            # 1. CEK ANOMALI (ANTI FRAUD)
            if cycles > 700 and curr_health > 90:
                res["user_behavior"] = "⚠️ SUSPICIOUS / MODIFIED"
                res["behavior_desc"] = f"DATA TIDAK WAJAR! Cycle {cycles} tapi Health {curr_health}%. Indikasi kuat baterai pernah diganti (Non-Ori) atau dimodifikasi (Suntikan)."
                res["behavior_color"] = "text-red-600"
                daily_factor = 1.0

            # 2. CEK SUPER USER (Health > 100%)
            elif curr_health > 100:
                res["user_behavior"] = "🦄 SUPER USER"
                res["behavior_desc"] = f"Unit Langka! Health {curr_health}% walau Cycle {cycles}. Hoki parah!"
                res["behavior_color"] = "text-purple-600"
                daily_factor = 1.5 

            # 3. [BARU] CEK CONTENT CREATOR / PRO USER
            # Logic: Cycle udah banyak (>300) TAPI Health masih Prima (>90%)
            # Artinya: Dipake kerja keras (1.8x cas/hari) tapi terawat.
            elif cycles > 300 and curr_health >= 90:
                res["user_behavior"] = "🎥 CONTENT CREATOR / PRO"
                res["behavior_desc"] = "Performa Tinggi! Cycle tinggi tapi kesehatan baterai terjaga. Definisi 'Device dipakai kerja keras'."
                res["behavior_color"] = "text-cyan-600" # Warna Baru: Cyan (Profesional)
                daily_factor = 1.8 # Asumsi ngecas hampir 2x sehari

            # 4. CEK HP BARU
            elif cycles <= 30:
                res["user_behavior"] = "🆕 FRESH UNIT"
                res["behavior_desc"] = "Unit sangat baru. Belum terbentuk pola pemakaian."
                res["behavior_color"] = "text-gray-500"
                daily_factor = 1.0 
            
            # 5. CEK DEGRADASI (Sisa User Lainnya)
            elif degrade_rate > 0.045: 
                res["user_behavior"] = "🔥 HARDCORE GAMER"
                res["behavior_desc"] = "Intensitas Tinggi! Sering dipakai berat sambil charging."
                res["behavior_color"] = "text-red-600"
                daily_factor = 2.3 
                
            elif degrade_rate > 0.035:
                res["user_behavior"] = "⚡ HEAVY USER"
                res["behavior_desc"] = "Pemakaian aktif seharian. Produktivitas tinggi."
                res["behavior_color"] = "text-orange-500"
                daily_factor = 1.6
                
            # Kita perketat syarat Sultan (harus < 0.012 degradasinya)
            elif degrade_rate < 0.012:
                res["user_behavior"] = "💎 SULTAN (LIGHT USER)"
                res["behavior_desc"] = "Pemakaian sangat apik. Suhu terjaga, jarang ngecas."
                res["behavior_color"] = "text-green-600"
                daily_factor = 0.8 
                
            else:
                res["user_behavior"] = "✅ DAILY DRIVER"
                res["behavior_desc"] = "Pemakaian wajar standar harian."
                res["behavior_color"] = "text-blue-600"
                daily_factor = 1.1
            # Umur = Cycles / Faktor Kebiasaan
            estimated_days = int(cycles / daily_factor)
            
            # Format Teks Umur
            age_text = ""
            if estimated_days < 30: age_text = f"± {estimated_days} Hari"
            elif estimated_days < 365: age_text = f"± {estimated_days//30} Bulan"
            else: age_text = f"± {estimated_days/365:.1f} Tahun"
            
            # Kita tambahkan detail faktornya biar kelihatan pinter
            res["age_estimation"] = f"{age_text} (Usage: {daily_factor}x/day)"

        except Exception as e:
            print(f"Error Profiling: {e}")

    res["hardware_issue"] = "Terdeteksi" if is_panic or "Missing sensor" in content else "Normal"

    res["processor"] = SOC_DB.get(hw_code, "Unknown Chipset")
    
    return res

# --- ROUTING WEB FLASK ---
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file: return jsonify({"error": "No file"}), 400
        try:
            content = file.read().decode('utf-8', errors='ignore')
            return jsonify(parse_ips_data(content))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
