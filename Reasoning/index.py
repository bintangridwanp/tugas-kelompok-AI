# -----------------------------------------
# Program Fuzzy Logic untuk Memilih 5 Restoran Terbaik
# Tanpa Menggunakan Library
# -----------------------------------------

# Fungsi untuk membaca data restoran dari CSV
def read_restaurants(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:  # skip header
            parts = line.strip().split(',')
            id_restoran = int(parts[0].replace('"','').strip())
            kualitas_servis = int(parts[1].replace('"','').strip())
            harga = float(parts[2].replace('"','').strip())
            data.append((id_restoran, kualitas_servis, harga))
    return data

# Fungsi Membership (fungsi keanggotaan) untuk Kualitas Servis
def kualitas_servis_membership(kualitas):
    buruk = max(0, min(1, (50 - kualitas) / 50))
    cukup = max(0, min((kualitas - 30) / 20, (70 - kualitas) / 20))
    bagus = max(0, min(1, (kualitas - 50) / 50))
    return {'buruk': buruk, 'cukup': cukup, 'bagus': bagus}

# Fungsi Membership untuk Harga
def harga_membership(harga):
    murah = max(0, min(1, (40000 - harga) / 15000))
    sedang = max(0, min((harga - 30000) / 10000, (50000 - harga) / 10000))
    mahal = max(0, min(1, (harga - 45000) / 10000))
    return {'murah': murah, 'sedang': sedang, 'mahal': mahal}

# Fungsi Inferensi Aturan
def inferensi(servis, harga):
    aturan = []
    # Contoh beberapa aturan:
    aturan.append(('sangat layak', min(servis['bagus'], harga['murah'])))
    aturan.append(('layak', min(servis['bagus'], harga['sedang'])))
    aturan.append(('cukup layak', min(servis['cukup'], harga['murah'])))
    aturan.append(('tidak layak', min(servis['buruk'], harga['mahal'])))
    # dan seterusnya sesuai logika fuzzy kamu
    return aturan

# Fungsi Defuzzification (Centroid Method)
def defuzzification(aturan):
    skor = 0
    total_bobot = 0
    nilai = {
        'sangat layak': 90,
        'layak': 75,
        'cukup layak': 60,
        'tidak layak': 40,
        'sangat tidak layak': 20
    }
    for kategori, nilai_keanggotaan in aturan:
        skor += nilai[kategori] * nilai_keanggotaan
        total_bobot += nilai_keanggotaan
    if total_bobot == 0:
        return 0
    return skor / total_bobot

# Fungsi Menyimpan hasil ke file
def save_result(filename, data):
    with open(filename, 'w') as file:
        file.write("ID,Kualitas Servis,Harga,Skor\n")
        for item in data:
            file.write("{},{},{},{}\n".format(item[0], item[1], item[2], item[3]))

# MAIN PROGRAM
if __name__ == "__main__":
    restoran = read_restaurants("restoran.csv")
    hasil = []

    for data in restoran:
        id_restoran, kualitas, harga = data
        servis_membership = kualitas_servis_membership(kualitas)
        harga_membership_value = harga_membership(harga)
        hasil_inferensi = inferensi(servis_membership, harga_membership_value)
        skor = defuzzification(hasil_inferensi)
        hasil.append((id_restoran, kualitas, harga, skor))

    # Urutkan berdasarkan skor terbesar
    hasil.sort(key=lambda x: x[3], reverse=True)

    # Ambil 5 restoran terbaik
    terbaik = hasil[:5]

    # Simpan ke file
    save_result("peringkat.csv", terbaik)

    # Tampilkan
    for item in terbaik:
        print(f"ID: {item[0]}, Kualitas Servis: {item[1]}, Harga: {item[2]}, Skor: {item[3]:.2f}")
