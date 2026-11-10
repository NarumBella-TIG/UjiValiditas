# Pengujian Validitas dan Reliabilitas Instrumen

Tugas mata kuliah **Probabilitas dan Statistika**, Program Studi Teknik Informatika, Politeknik Caltex Riau.

**M. Narum Bella** (2455301225), 3 TI F

Uji validitas (korelasi Pearson butir-total, r tabel pada α = 0,05) dan reliabilitas (Cronbach's alpha) terhadap
*Kuesioner Penggunaan AI dan Lifestyle Media Sosial Mahasiswa*, dengan responden kelas 3 TI F (n = 30).
Kuesioner terdiri atas dua bagian, dan setiap bagian dianalisis pada notebook tersendiri.

| Bagian | Notebook | Dimensi |
| --- | --- | --- |
| Penggunaan AI | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NarumBella-TIG/UjiValiditas/blob/main/uji_validitas_penggunaan_ai.ipynb) `uji_validitas_penggunaan_ai.ipynb` | Penggunaan AI, Aspek Psikologis (14 butir) |
| Lifestyle Media Sosial | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NarumBella-TIG/UjiValiditas/blob/main/uji_validitas_lifestyle_media_sosial.ipynb) `uji_validitas_lifestyle_media_sosial.ipynb` | Kebiasaan Teknologi Digital, Prokrastinasi Akademik, Respon Emosional (15 butir) |

## Isi

| File | Isi |
| --- | --- |
| `uji_validitas_penggunaan_ai.ipynb` / `.py` | Langkah 1-8 modul dan Latihan 1-4 untuk bagian Penggunaan AI |
| `uji_validitas_lifestyle_media_sosial.ipynb` / `.py` | Langkah 1-8 modul dan Latihan 1-4 untuk bagian Lifestyle Media Sosial |
| `Dataset_Kuesioner_3TIF.xlsx` | Data respons kuesioner kelas 3 TI F (jawaban berupa label Likert) |
| `hasil_uji_penggunaan_ai.xlsx` | Hasil Langkah 8 bagian Penggunaan AI (sheet Validitas dan Reliabilitas) |
| `hasil_uji_lifestyle_media_sosial.xlsx` | Hasil Langkah 8 bagian Lifestyle Media Sosial |

## Cara menjalankan

Klik **Open in Colab** pada bagian yang ingin dianalisis, pilih *Runtime > Run all*, lalu unggah
`Dataset_Kuesioner_3TIF.xlsx` saat diminta pada Langkah 2. File hasil akan terunduh otomatis di akhir.

## Ringkasan hasil

| Bagian | Dimensi | Butir | Cronbach's alpha | Kategori |
| --- | --- | --- | --- | --- |
| Penggunaan AI | Penggunaan AI | 7 | 0,799 | Reliabel |
| Penggunaan AI | Aspek Psikologis | 7 | 0,886 | Baik |
| Lifestyle Media Sosial | Kebiasaan Teknologi Digital | 6 | 0,890 | Baik |
| Lifestyle Media Sosial | Prokrastinasi Akademik | 4 | 0,860 | Baik |
| Lifestyle Media Sosial | Respon Emosional | 5 | 0,928 | Sangat baik |

Seluruh 29 butir valid (r hitung > r tabel 0,361) dan kelima dimensi reliabel (α ≥ 0,70).

## Penggunaan AI

Penyusunan kode dibantu Claude (Anthropic). Mahasiswa bertanggung jawab atas kode, hasil analisis, dan kesimpulan.
