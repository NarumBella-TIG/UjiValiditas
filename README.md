# Pengujian Validitas dan Reliabilitas Instrumen

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NarumBella-TIG/UjiValiditas/blob/main/uji_validitas_reliabilitas.ipynb)

Tugas mata kuliah **Probabilitas dan Statistika**, Program Studi Teknik Informatika, Politeknik Caltex Riau.

**M. Narum Bella** (2455301225), 3 TI F

Uji validitas (korelasi Pearson butir-total, r tabel pada α = 0,05) dan reliabilitas (Cronbach's alpha) terhadap
kuesioner penggunaan AI, kebiasaan teknologi digital, prokrastinasi akademik, dan respon emosional, khusus
responden kelas 3 TI F (n = 30, 5 dimensi, 29 butir).

## Isi

| File | Isi |
| --- | --- |
| `uji_validitas_reliabilitas.ipynb` | Notebook Google Colab: Langkah 1-8 modul dan Latihan 1-4, lengkap dengan output |
| `uji_validitas_reliabilitas.py` | Kode yang sama dalam bentuk skrip Python |
| `Dataset_Kuesioner_3TIF.xlsx` | Data respons kuesioner kelas 3 TI F (jawaban berupa label Likert) |
| `hasil_uji_validitas_reliabilitas.xlsx` | Hasil Langkah 8: sheet Validitas dan Reliabilitas |

## Cara menjalankan

Klik **Open in Colab**, pilih *Runtime > Run all*, lalu unggah `Dataset_Kuesioner_3TIF.xlsx` saat diminta pada
Langkah 2. File `hasil_uji_validitas_reliabilitas.xlsx` akan terunduh otomatis di akhir.

## Ringkasan hasil

| Dimensi | Butir | Cronbach's alpha | Kategori |
| --- | --- | --- | --- |
| Penggunaan AI | 7 | 0,625 | Tidak reliabel |
| Aspek Psikologis | 7 | 0,643 | Tidak reliabel |
| Kebiasaan Teknologi Digital | 6 | 0,674 | Tidak reliabel |
| Prokrastinasi Akademik | 4 | 0,900 | Sangat baik |
| Respon Emosional | 5 | 0,764 | Reliabel |

Seluruh 29 butir valid (r hitung > r tabel 0,361).

## Penggunaan AI

Penyusunan kode dibantu Claude (Anthropic). Mahasiswa bertanggung jawab atas kode, hasil analisis, dan kesimpulan.
