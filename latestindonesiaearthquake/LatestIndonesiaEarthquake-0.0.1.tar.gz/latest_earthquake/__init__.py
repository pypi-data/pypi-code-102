import requests
from bs4 import BeautifulSoup


def ekstraksi_data():
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        # tgl = soup.find('span', {'class': 'waktu'})
        # tgl = tgl.text.split(', ')
        # tanggal = tgl[0]
        # waktu = tgl[1]

        gempa = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        gempa = gempa.findChildren('li')
        i = 0
        for res in gempa:
            if i == 0:
                tgl = res.text.split(', ')
                tanggal = tgl[0]
                waktu = tgl[1]
            elif i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                lokasi = res.text.split(' - ')
                ls = lokasi[0]
                bt = lokasi[1]
            elif i == 4:
                pusat = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasil = dict()
        hasil['tanggal'] = tanggal
        hasil['waktu'] = waktu
        hasil['magnitudo'] = magnitudo
        hasil['kedalaman'] = kedalaman
        hasil['ls'] = ls
        hasil['bt'] = bt
        hasil['pusat_gempa'] = pusat
        hasil['dirasakan_skala_mmi'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("Tidak bisa mendapatkan data")
        return
    print('Gempa terkini berdasarkan BMKG')
    print(f"Tanggal: {result['tanggal']}")
    print(f"Waktu : {result['waktu']}")
    print(f"Magnitudo : {result['magnitudo']}")
    print(f"Kedalaman : {result['kedalaman']}")
    print(f"Lokasi : {result['ls']} {result['bt']}")
    print(f"{result['pusat_gempa']}")
    print(f"{result['dirasakan_skala_mmi']}")


if __name__ == '__main__':
    result = ekstraksi_data()
    tampilkan_data(result)
