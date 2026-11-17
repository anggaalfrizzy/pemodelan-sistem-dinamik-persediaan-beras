# Pemodelan Sistem Dinamik Persediaan Beras Rumah Tangga

Project mata kuliah Pemodelan Sistem Dinamik: simulasi stok beras rumah tangga akibat pemakaian dan pembelian
menggunakan Python (SciPy `odeint` dan GEKKO).

## Isi
- `src/` : program Python (01-08)
- `notebook/` : notebook Google Colab
- `figs/` : grafik hasil simulasi
- `docs/` : laporan project dan tutorial (docx)

## Cara menjalankan
```
pip install -r requirements.txt
python src/01_pembelian_saja.py
```
Atau buka notebook di Google Colab dan jalankan sel dari atas ke bawah.

## Model
dS/dt = k_b*u_b(t) - k_c*u_c(t) - k_s*S(t), dengan S = stok beras (kg), u_b = intensitas pembelian (%), u_c = intensitas pemakaian (%).

Tautan: Colab [isi tautan] | YouTube [isi tautan]
