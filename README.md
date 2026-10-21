# Sesi 6 — Forest Change Monitor
**Topik seminar:** Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI  
**Studi kasus:** Pemantauan Perubahan Tutupan Hutan dan Klasifikasi Indikasi Pembukaan Lahan

## 1. Latar belakang
Peringatan perubahan tutupan lahan dapat menunjukkan lokasi dan waktu indikasi perubahan, tetapi tidak otomatis menjelaskan penyebabnya. Proyek demonstrasi ini memperlihatkan alur analisis sederhana: membandingkan indikator vegetasi sebelum/sesudah, memvisualisasikan sampel per zona, dan mencoba model klasifikasi.

## 2. Tujuan
- Mengeksplorasi indikator perubahan vegetasi pada data contoh.
- Memvisualisasikan sampel dan koordinat pada peta interaktif.
- Menjalankan model Decision Tree sederhana.
- Memahami evaluasi model dan batasan interpretasi.

## 3. Peringatan penting
`land_change_samples.csv` berisi **data sintetis**, bukan citra satelit asli. Koordinat hanya contoh demonstrasi dan label dibuat untuk latihan. Jangan mengklaim hasil ini sebagai pemantauan deforestasi nyata atau menggunakan labelnya untuk menuduh pihak tertentu.

## 4. Isi folder
- `app.py` — dashboard Streamlit.
- `data/land_change_samples.csv` — data sintetis.
- `requirements.txt` — dependensi Python.
- `README.md` — panduan proyek.

## 5. Langkah pengerjaan satu per satu
### Langkah 1 — Siapkan Python dan Git
Gunakan Python 3.10 atau lebih baru. Periksa:
```bash
python --version
git --version
```

### Langkah 2 — Ekstrak dan buka folder
Ekstrak ZIP lalu buka `sesi-6-monitoring-hutan` di VS Code atau terminal.

### Langkah 3 — Buat virtual environment (disarankan)
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Langkah 4 — Install dependensi
```bash
pip install -r requirements.txt
```

### Langkah 5 — Pelajari kolom dataset
- `ndvi_before` dan `ndvi_after`: indikator vegetasi contoh sebelum dan sesudah.
- `ndvi_drop`: besar penurunan NDVI contoh.
- `bare_soil_change`: perubahan indikator tanah terbuka sintetis.
- `burn_index_change`: perubahan indeks kebakaran sintetis.
- `label`: kelas latihan (`Stabil` atau `Pembukaan lahan`).
- `latitude` dan `longitude`: koordinat contoh untuk peta.

### Langkah 6 — Jalankan dashboard
```bash
streamlit run app.py
```
Buka alamat lokal yang ditampilkan oleh Streamlit.

### Langkah 7 — Eksplorasi data
1. Pilih satu atau beberapa zona di sidebar.
2. Atur penurunan NDVI minimum.
3. Amati perubahan kartu metrik dan grafik.
4. Jelajahi titik contoh pada peta.
5. Unduh data hasil filter untuk pemeriksaan lanjutan.

### Langkah 8 — Jalankan dan pahami model
Dashboard membagi data menjadi training dan testing, lalu melatih Decision Tree. Periksa akurasi dan confusion matrix. Karena data sintetis sangat kecil dan pola label dibuat sederhana, hasil evaluasi tidak mewakili kinerja pada citra satelit sungguhan.

### Langkah 9 — Pahami workflow untuk kasus nyata
Untuk mengembangkan sistem yang realistis, diperlukan:
1. Mengambil citra satelit yang sesuai dan memiliki tanggal yang jelas.
2. Melakukan cloud masking dan prapemrosesan yang relevan.
3. Membandingkan citra lintas waktu dengan kondisi yang sebanding.
4. Menyiapkan label referensi yang diverifikasi ahli.
5. Membagi data latih/uji secara tepat, menghindari kebocoran spasial.
6. Mengevaluasi precision, recall, F1-score, dan confusion matrix.
7. Menampilkan peringatan pada peta dengan tingkat ketidakpastian.
8. Memvalidasi temuan sebelum keputusan atau tindakan lapangan.

### Langkah 10 — Upload ke GitHub
1. Buat repository baru bernama `studi-kasus-monitoring-perubahan-hutan`.
2. Jalankan perintah berikut dari folder proyek:
```bash
git init
git add .
git commit -m "Add forest change monitoring case study"
git branch -M main
git remote add origin https://github.com/USERNAME/studi-kasus-monitoring-perubahan-hutan.git
git push -u origin main
```
3. Ganti `USERNAME` dengan username GitHub-mu. Pastikan repository sudah dibuat terlebih dahulu.

## 6. Pertanyaan analisis untuk laporan
1. Mengapa perubahan NDVI tidak selalu berarti deforestasi?
2. Apa risiko jika model dilatih dengan label yang salah atau tidak seimbang?
3. Mengapa hasil model harus diverifikasi sebelum ditindaklanjuti?
4. Apa perbedaan antara mendeteksi perubahan tutupan lahan dan mengidentifikasi penyebab langsungnya?

## 7. Kaitan dengan materi seminar
Proyek ini mengilustrasikan pemrosesan fitur, klasifikasi machine learning, evaluasi model, visualisasi peta, serta kebutuhan validasi. Sistem nyata membutuhkan citra satelit dan label tepercaya; demo ini hanya mempraktikkan struktur workflow.
