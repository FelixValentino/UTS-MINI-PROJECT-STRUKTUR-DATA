import time
import random
import os

def muatJadwal():
    daftarJadwal = []
    if not os.path.exists("jadwal.txt"):
        dataBawaan = (
            "101,Pesawat,Jakarta,Bali,08:00,1200000\n"
            "102,Pesawat,Jakarta,Bali,14:00,1500000\n"
            "103,Pesawat,Jakarta,Surabaya,10:00,800000\n"
            "104,Kereta,Jakarta,Surabaya,06:00,400000\n"
            "105,Kereta,Surabaya,Banyuwangi,13:00,200000\n"
            "106,Kapal,Banyuwangi,Bali,18:00,150000\n"
        )
        with open("jadwal.txt", "w") as file:
            file.write(dataBawaan)
            
    with open("jadwal.txt", "r") as file:
        for baris in file:
            if baris.strip():  
                idPerjalanan, moda, asal, tujuan, jam, harga = baris.strip().split(",")
                daftarJadwal.append([int(idPerjalanan), moda, asal, tujuan, jam, int(harga)])
    return daftarJadwal

def muatPenumpang():
    daftarPenumpang = []
    if not os.path.exists("penumpang.txt"):
        dataBawaan = (
            "PNR102,Budi,Jakarta-Bali,2B\n"
            "PNR105,Andi,Surabaya-Banyuwangi,4A\n"
            "PNR101,Siti,Jakarta-Surabaya,1C\n"
        )
        with open("penumpang.txt", "w") as file:
            file.write(dataBawaan)
            
    with open("penumpang.txt", "r") as file:
        for baris in file:
            if baris.strip():
                pnr, nama, rute, kursi = baris.strip().split(",")
                daftarPenumpang.append([pnr, nama, rute, kursi])
    return daftarPenumpang

def simpanPenumpangBaru(pnr, nama, rute, kursi):
    with open("penumpang.txt", "a") as file:  
        file.write(f"{pnr},{nama},{rute},{kursi}\n")

jadwalDB = muatJadwal()
dataPenumpang = muatPenumpang()

ruteTransitDB = {
    "Jakarta": [("Surabaya", "Kereta"), ("Bali", "Pesawat")],
    "Surabaya": [("Banyuwangi", "Kereta")],
    "Banyuwangi": [("Bali", "Kapal")],
    "Bali": []
}

kursiPesawat = [
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O'],
    ['O', 'O', 'O', 'O']
]
kolomMap = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
            
def sinkronisasiKursi():
    for b in range(5):
        for k in range(4):
            kursiPesawat[b][k] = 'O'
    
    for p in dataPenumpang:
        kodeKursi = p[3]  
        if len(kodeKursi) >= 2:
            bagianBaris = kodeKursi[:-1]   
            kodeHuruf = kodeKursi[-1].upper() 
            
            if bagianBaris.isdigit() and kodeHuruf in kolomMap:
                baris = int(bagianBaris) - 1
                kolom = kolomMap[kodeHuruf]
                
                if 0 <= baris < 5:
                    kursiPesawat[baris][kolom] = 'X'

sinkronisasiKursi()

def cetakKursi():
    print("\nDenah Kursi Pesawat")
    print("    A  B  C  D")
    for i, baris in enumerate(kursiPesawat):
        print(f"{i + 1}  " + "  ".join(baris))
    print("Keterangan : O = Kosong, X = Terisi")

# Cari & Pesan Tiket

def cariRuteLangsung(asal, tujuan):
    hasil = []
    for i in jadwalDB:
        if i[2].lower() == asal.lower() and i[3].lower() == tujuan.lower():
            hasil.append(i)
    return hasil
    
def cariRuteTransit(sekarang, tujuan, jalurSaatIni=[]):
    jalurSaatIni = jalurSaatIni + [sekarang]
    if sekarang.lower() == tujuan.lower():
        return [jalurSaatIni]
    if sekarang not in ruteTransitDB:
        return []
    
    semuaJalur = []
    for (tetangga, moda) in ruteTransitDB[sekarang]:
        if tetangga not in jalurSaatIni:
            jalurBaru = cariRuteTransit(tetangga, tujuan, jalurSaatIni)
            for i in jalurBaru:
                semuaJalur.append(i)
    return semuaJalur
    
def hitungTotal(daftarUmur, hargaDasar, index=0):
    if index == len(daftarUmur):
        return 0
    
    umur = daftarUmur[index]
    if umur < 12:
        hargaTiket = hargaDasar * 0.5
    else:
        hargaTiket = hargaDasar
        
    return hargaTiket + hitungTotal(daftarUmur, hargaDasar, index + 1)

# Lihat Jadwal & Urutkan Harga

def Jadwal(jadwalList):
    n = len(jadwalList)
    for i in range(n):
        for j in range(0, n - i - 1):
            if jadwalList[j][5] > jadwalList[j + 1][5]:
                jadwalList[j], jadwalList[j + 1] = jadwalList[j + 1], jadwalList[j]
    return jadwalList

# Verifikasi Kode Booking

def Verifikasi(kodeCari):
    dataUrut = sorted(dataPenumpang, key=lambda x: x[0])
    
    low = 0
    high = len(dataUrut) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if dataUrut[mid][0] == kodeCari:
            return dataUrut[mid]
        elif dataUrut[mid][0] < kodeCari:
            low = mid + 1
        else:
            high = mid - 1
    return None

# Analisis Efisiensi (Big O)
    
def Analisis():
    print("===== Big O Analisis =====")
    
    ukuranData = 5000
    dataStress = [["PNR" + str(random.randint(10000,99999)), "User", "A-B", "1A"] for _ in range(ukuranData)]
    targetCari = dataStress[-1][0]
    
    startTime = time.time()
    for i in dataStress:
        if i[0] == targetCari:
            break
    linearTime = time.time() - startTime
    print(f"Linear Search pada {ukuranData} data (Worst Case): {linearTime:.6f} detik -> O(N)")
    
    startTime = time.time()
    dataStress.sort(key=lambda X: X[0])
    low, high = 0, len(dataStress) - 1
    while low <= high:
        mid = (low + high) // 2
        if dataStress[mid][0] == targetCari:
            break
        elif dataStress[mid][0] < targetCari:
            low = mid + 1
        else:
            high = mid - 1
    binaryTime = time.time() - startTime
    print(f"Binary Search + Sort pada {ukuranData} data     : {binaryTime:.6f} detik -> O(N log N)")
    print("Kesimpulan: Binary Search jauh lebih efisien pada data skala besar setelah di-sorting.")

def Menu():
    print("\n==== MULTI-MODAL TRANSPORTATION BOOKING SYSTEM =====")
    print("1. Cari & Pesan Tiket")
    print("2. Lihat Jadwal & Urutkan Harga")
    print("3. Verifikasi Kode Booking")
    print("4. Analisis Efisiensi (Big O)")
    print("5. Exit")
    
def menuCariPesanTiket():
    global dataPenumpang
    print("\n===== Cari & Pesan Tiket =====")
    asal = input("Masukkan Kota Asal (Contoh : Jakarta) : ")
    tujuan = input("Masukkan Kota Tujuan (Contoh : Bali) : ")
    
    hasil = cariRuteLangsung(asal, tujuan)
    
    if hasil:
        print("Rute Langsung Ditemukan")
        for i in hasil:
            print(f"[{i[0]}] {i[1]} | {i[2]} -> {i[3]} | Jam {i[4]} | Rp {i[5]:,}")
        
        pilihID = int(input("Masukkan ID perjalanan yang ingin dipesan : "))
        pilihJadwal = next((x for x in hasil if x[0] == pilihID), None)
        
        if pilihJadwal:
            jumlahPenumpang = int(input("Masukkan jumlah penumpang : "))
            daftarUmur = []
            for i in range(jumlahPenumpang):
                umur = int(input(f"Masukkan umur penumpang ke-{i + 1} : "))
                daftarUmur.append(umur)
            
            totalHarga = hitungTotal(daftarUmur, pilihJadwal[5])
            print(f"Total Biaya Tiket : Rp {totalHarga:,}")
            
            cetakKursi()
            baris = int(input("Masukkan Baris (1-5) : ")) - 1
            kolomHuruf = input("Masukkan Kolom (A-D) : ").upper()
            kolom = kolomMap.get(kolomHuruf, -1)
            
            if 0 <= baris < 5 and kolom != -1:
                if kursiPesawat[baris][kolom] == 'O':
                    kursiPesawat[baris][kolom] = 'X'
                    kodePNR = "PNR" + str(random.randint(100, 999))
                    namaPenumpang = input("Masukkan Nama Anda : ")
                    simpanPenumpangBaru(kodePNR, namaPenumpang, f"{asal}-{tujuan}", f"{baris + 1}{kolomHuruf}")
                    dataPenumpang.append([kodePNR, namaPenumpang, f"{asal}-{tujuan}", f"{baris + 1}{kolomHuruf}"])
                    sinkronisasiKursi()
                    print(f"Booking Berhasil, Kode Tiket Anda : {kodePNR}")
                else:
                    print("Maaf kursi tersebut sudah terisi")
            else:
                print("Koordinat kursi tidak valid")
    else:
        print("Tidak ada rute langsung, mencari alternatif rute transit")
        jalurTransit = cariRuteTransit(asal, tujuan)
        if jalurTransit:
            print("Rute transit yang tersedia")
            for i, rute in enumerate(jalurTransit):
                print(f"Alternatif {i + 1} : " + " -> ".join(rute))
        else:
            print("Maaf tidak ada rute langsung maupun transit")
            
def menuLihatJadwal():
    print("\n===== Lihat Jadwal & Urutkan Harga =====")
    print("\nJadwal Sebelum di Sortir")
    for i in jadwalDB:
        print(f"[{i[0]}] {i[1]} | {i[2]} -> {i[3]} | Rp {i[5]:,}")
        
    print("Mengurutkan jadwal berdasarkan harga termurah")
    jadwalSort = Jadwal(jadwalDB.copy())
    
    print("Jadwal Setelah di Sortir")
    for i in jadwalSort:
        print(f"[{i[0]}] {i[1]} | {i[2]} -> {i[3]} | Rp {i[5]:,}")
        
def menuVerifikasiBooking():
    print("\n===== Verifikasi Kode Booking =====")
    kode = input("Masukkan kode booking yang dicari (Contoh : PNR102) : ").upper()
    data = Verifikasi(kode)
    if data:
        print("Data Tiket Ditemukan")
        print(f"Kode Booking : {data[0]}")
        print(f"Nama         : {data[1]}")
        print(f"Rute         : {data[2]}")
        print(f"Nomor Kursi  : {data[3]}")
    else:
        print("Kode Booking tidak terdaftar")
        
def menuAnalisisEfisiensi():
    print("\n===== Analisis Efisiensi (Big O) =====")
    Analisis()
    
def Main():
    while True:
        Menu()
        
        pilihan = int(input("Masukkan Pilihan : "))
        
        if pilihan == 1:
            menuCariPesanTiket()
            
        elif pilihan == 2:
            menuLihatJadwal()
            
        elif pilihan == 3:
            menuVerifikasiBooking()
            
        elif pilihan == 4:
            menuAnalisisEfisiensi()
            
        elif pilihan == 5:
            print("Thankyou")
            break
        
        else:
            print("Invalid")
            
            
if __name__ == "__main__":
    Main()