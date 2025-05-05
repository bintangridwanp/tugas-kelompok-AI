import csv

def fuzzify_servis(servis):
    result = {}
    if servis <= 50:
        result["rendah"] = 1
    elif 50 < servis < 70:
        result["rendah"] = (70 - servis) / 20
    else:
        result["rendah"] = 0

    if 60 < servis < 75:
        result["sedang"] = (servis - 60) / 15
    elif 75 <= servis <= 90:
        result["sedang"] = (90 - servis) / 15
    else:
        result["sedang"] = 0

    if servis >= 100:
        result["tinggi"] = 1
    elif 80 < servis < 100:
        result["tinggi"] = (servis - 80) / 20
    else:
        result["tinggi"] = 0

    return result

def fuzzify_harga(harga):
    result = {}
    if harga <= 10000:
        result["murah"] = 1
    elif 10000 < harga < 25000:
        result["murah"] = (25000 - harga) / 15000
    else:
        result["murah"] = 0

    if 15000 < harga < 30000:
        result["sedang"] = (harga - 15000) / 15000
    elif 30000 <= harga < 45000:
        result["sedang"] = (45000 - harga) / 15000
    else:
        result["sedang"] = 0

    if harga >= 50000:
        result["mahal"] = 1
    elif 20000 < harga < 50000:
        result["mahal"] = (harga - 20000) / 30000
    else:
        result["mahal"] = 0

    return result

def inference(servis_fz, harga_fz):
    rules = []
    rules.append(("tinggi", min(servis_fz["tinggi"], harga_fz["murah"])))
    rules.append(("sedang", min(servis_fz["sedang"], harga_fz["murah"])))
    rules.append(("rendah", min(servis_fz["rendah"], harga_fz["mahal"])))
    rules.append(("sedang", min(servis_fz["tinggi"], harga_fz["mahal"])))
    rules.append(("rendah", min(servis_fz["rendah"], harga_fz["murah"])))
    rules.append(("sedang", min(servis_fz["sedang"], harga_fz["sedang"])))

    return rules

def defuzzification(inferensi):
    nilai = 0.0
    bobot = 0.0
    for label, val in inferensi:
        if label == "tinggi":
            nilai += val * 90
        elif label == "sedang":
            nilai += val * 70
        elif label == "rendah":
            nilai += val * 50
        bobot += val
    return nilai / bobot if bobot != 0 else 0

def main():
    data = []
    with open("restoran.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = int(row["id Pelanggan"])
            servis = int(row["Pelayanan"])
            harga = int(row["harga"])

            servis_fz = fuzzify_servis(servis)
            harga_fz = fuzzify_harga(harga)
            infer = inference(servis_fz, harga_fz)
            skor = defuzzification(infer)

            data.append((id, servis, harga, skor))

    top5 = sorted(data, key=lambda x: x[3], reverse=True)[:5]

    print("Top 5 Restoran Terbaik Berdasarkan Fuzzy:")
    print("| ID  | Servis | Harga  | Skor |")
    print("|-----|--------|--------|------|")
    for id, servis, harga, skor in top5:
        print(f"| {id:3} | {servis:6} | {harga:6} | {skor:.2f} |")
    print("\nRekomendasi Restoran:")
    for id, servis, harga, skor in top5:
        print(f"ID: {id}, Servis: {servis}, Harga: {harga}, Skor: {skor:.2f}")
main()