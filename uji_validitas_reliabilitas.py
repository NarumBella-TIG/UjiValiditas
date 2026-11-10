# %% [markdown]
# # Pengujian Validitas dan Reliabilitas Instrumen
#
# **Probabilitas dan Statistika** · M. Narum Bella (2455301225) · 3 TI F · Politeknik Caltex Riau
#
# Data: respons kuesioner penggunaan AI, kebiasaan digital, prokrastinasi akademik, dan respon emosional
# **khusus kelas 3 TI F** (`Dataset_Kuesioner_3TIF.xlsx`, jawaban masih berupa label seperti "Setuju (S)").
#
# Langkah 1-8 mengikuti modul, dengan dua penyesuaian terhadap data:
# - kolom demografi berjumlah 6 (Timestamp, Score, Kelas, Jenis Kelamin, dan 2 kolom jumlah platform AI);
# - kolom "Durasi (jam) rata-rata penggunaan gadget" berada di tengah butir tetapi bukan butir Likert,
#   sehingga dikeluarkan dari analisis.

# %% [markdown]
# ## Langkah 1: Persiapan lingkungan dan impor pustaka

# %%
import re
import pandas as pd
import numpy as np
from scipy import stats

# %% [markdown]
# ## Langkah 2: Unggah berkas data
# Di Google Colab akan muncul tombol **Choose Files**; pilih `Dataset_Kuesioner_3TIF.xlsx`.

# %%
try:
    from google.colab import files
    up = files.upload()
    nama_file = list(up.keys())[0]
except ImportError:                                   # jika dijalankan di luar Colab
    nama_file = "Dataset_Kuesioner_3TIF.xlsx"
print("File terbaca:", nama_file)

# %% [markdown]
# ## Langkah 3: Membaca data dan memisahkan butir

# %%
JUMLAH_KOLOM_DEMOGRAFI = 6   # Timestamp, Score, Kelas, Jenis Kelamin, 2 kolom jumlah platform AI

df = pd.read_excel(nama_file)
df = df[df["Kelas"].astype(str).str.strip() == "3 TI F"].reset_index(drop=True)   # analisis khusus 3 TI F
butir = df.iloc[:, JUMLAH_KOLOM_DEMOGRAFI:]

# Kolom durasi gadget bukan butir Likert (isinya "4 - 7 jam", dst.), jadi dikeluarkan
kolom_bukan_butir = [k for k in butir.columns if not re.match(r"^(.*?) \[", k)]
print("Kolom non-butir yang dikeluarkan:", kolom_bukan_butir)
butir = butir.drop(columns=kolom_bukan_butir)

print("Jumlah responden :", len(df))
print("Jumlah butir     :", butir.shape[1])
print("Data kosong      :", int(butir.isna().sum().sum()))
print("Responden per kelas:", df["Kelas"].value_counts().to_dict())

# %% [markdown]
# ## Langkah 4: Mengubah jawaban Likert menjadi angka
# Label jawaban diubah menjadi angka: STS = 1, TS = 2, N = 3, S = 4, SS = 5.

# %%
skala = {
    "Sangat Tidak Setuju (STS)": 1,
    "Tidak Setuju (TS)": 2,
    "Netral (N)": 3,
    "Setuju (S)": 4,
    "Sangat Setuju (SS)": 5,
}

num = butir.replace(skala).apply(pd.to_numeric, errors="coerce")

# Harus 0. Jika lebih dari 0, ada jawaban yang tidak terbaca.
print("Sel yang gagal dikonversi:", int(num.isna().sum().sum()))
print("Nilai yang muncul:", sorted(int(v) for v in pd.unique(num.values.ravel())))
# 5 responden pertama; judul kolom disingkat K1-K29 agar tabel muat di layar
num.head().set_axis([f"K{i}" for i in range(1, num.shape[1] + 1)], axis=1)

# %% [markdown]
# ## Langkah 5: Mengelompokkan butir per dimensi

# %%
dimensi = {}
for kolom in butir.columns:
    nama = re.match(r"^(.*?) \[", kolom).group(1).strip().rstrip(".")
    dimensi.setdefault(nama, []).append(kolom)

for nama, daftar in dimensi.items():
    print(f"{nama}: {len(daftar)} butir")

# Kode butir tetap (B1, B2, ...) agar nomor tidak bergeser saat ada butir yang dibuang
KODE = {kolom: f"B{i}" for nama, daftar in dimensi.items() for i, kolom in enumerate(daftar, 1)}

# Daftar kode butir dan pernyataannya
kamus_butir = pd.DataFrame([
    {"Dimensi": nama, "Butir": f"B{i}", "Pernyataan": kolom[kolom.index("[") + 1:].rstrip("]")}
    for nama, daftar in dimensi.items() for i, kolom in enumerate(daftar, 1)
])
kamus_butir

# %% [markdown]
# ## Langkah 6: Uji validitas (korelasi Pearson butir-total)

# %%
def r_tabel_untuk(n, alpha=0.05):
    t = stats.t.ppf(1 - alpha / 2, n - 2)
    return t / np.sqrt((n - 2) + t**2)


def uji_validitas(num, dimensi):
    n = len(num)
    r_tabel = r_tabel_untuk(n)
    hasil = []
    for nama, daftar in dimensi.items():
        x = num[daftar]
        total = x.sum(axis=1)
        for i, kolom in enumerate(daftar, 1):
            r, p = stats.pearsonr(x[kolom], total)
            r_koreksi, _ = stats.pearsonr(x[kolom], total - x[kolom])
            hasil.append({
                "Dimensi": nama,
                "Butir": KODE[kolom],
                "r hitung": round(r, 3),
                "Corrected r": round(r_koreksi, 3),
                "p-value": round(p, 4),
                "Keterangan": "Valid" if r > r_tabel else "Tidak valid",
            })
    return pd.DataFrame(hasil), r_tabel


tabel_validitas, r_tabel = uji_validitas(num, dimensi)
print(f"n = {len(num)} | r tabel (α=0,05; df={len(num) - 2}) = {r_tabel:.3f}")
print("Butir valid:", (tabel_validitas["Keterangan"] == "Valid").sum(), "dari", len(tabel_validitas))
tabel_validitas

# %% [markdown]
# ## Langkah 7: Uji reliabilitas (Cronbach's alpha)

# %%
def cronbach_alpha(x):
    k = x.shape[1]
    return k / (k - 1) * (1 - x.var(ddof=1).sum() / x.sum(axis=1).var(ddof=1))


def kategori(a):
    return ("Sangat baik" if a >= 0.90 else "Baik" if a >= 0.80
            else "Reliabel" if a >= 0.70 else "Tidak reliabel")


def uji_reliabilitas(num, dimensi):
    hasil_reliabilitas, alpha_dihapus = [], []
    for nama, daftar in dimensi.items():
        x = num[daftar]
        a = cronbach_alpha(x)
        hasil_reliabilitas.append({"Dimensi": nama, "Jumlah butir": len(daftar),
                                   "Cronbach's alpha": round(a, 3), "Kategori": kategori(a)})
        for i, kolom in enumerate(daftar, 1):
            if len(daftar) > 2:
                alpha_dihapus.append({"Dimensi": nama, "Butir": KODE[kolom],
                                      "Alpha jika dihapus": round(cronbach_alpha(x.drop(columns=kolom)), 3)})
    return pd.DataFrame(hasil_reliabilitas), pd.DataFrame(alpha_dihapus)


tabel_reliabilitas, tabel_alpha_dihapus = uji_reliabilitas(num, dimensi)
display(tabel_reliabilitas)
display(tabel_alpha_dihapus)

# %% [markdown]
# ## Langkah 8: Menggabungkan dan mengunduh hasil
# Kolom tambahan "Keputusan" mengikuti tabel pedoman pengambilan keputusan pada modul (bagian 6).

# %%
gabung = tabel_validitas.merge(tabel_alpha_dihapus, on=["Dimensi", "Butir"], how="left")
alpha_dimensi = tabel_reliabilitas.set_index("Dimensi")["Cronbach's alpha"]


def keputusan(baris):
    valid = baris["Keterangan"] == "Valid"
    naik = baris["Alpha jika dihapus"] > alpha_dimensi[baris["Dimensi"]]
    if valid and not naik:
        return "Pertahankan"
    if valid and naik:
        return "Tinjau isi butir"
    if not valid and naik:
        return "Buang atau revisi"
    return "Tinjau ulang sebelum dibuang"


gabung["Keputusan"] = gabung.apply(keputusan, axis=1)
gabung = gabung.merge(kamus_butir, on=["Dimensi", "Butir"])

with pd.ExcelWriter("hasil_uji_validitas_reliabilitas.xlsx") as w:
    gabung.to_excel(w, sheet_name="Validitas", index=False)
    tabel_reliabilitas.to_excel(w, sheet_name="Reliabilitas", index=False)

try:
    files.download("hasil_uji_validitas_reliabilitas.xlsx")
except NameError:
    print("Tersimpan: hasil_uji_validitas_reliabilitas.xlsx")
gabung[["Dimensi", "Butir", "r hitung", "Corrected r", "Alpha jika dihapus", "Keputusan"]]

# %% [markdown]
# ## Latihan 1: Butir yang tidak valid

# %%
tidak_valid = tabel_validitas[tabel_validitas["Keterangan"] == "Tidak valid"]
print(f"r tabel = {r_tabel:.3f}")
if tidak_valid.empty:
    terendah = tabel_validitas.loc[tabel_validitas["r hitung"].idxmin()]
    print("Tidak ada butir yang tidak valid; semua r hitung > r tabel.")
    print(f"r hitung terendah: {terendah['Dimensi']} {terendah['Butir']} = {terendah['r hitung']}")
else:
    display(tidak_valid)

# %% [markdown]
# ## Latihan 2: Perbandingan kriteria r hitung dan corrected r ≥ 0,30

# %%
valid_r = (tabel_validitas["r hitung"] > r_tabel).sum()
valid_rc = (tabel_validitas["Corrected r"] >= 0.30).sum()
print(f"Valid menurut r hitung > {r_tabel:.3f}      : {valid_r} butir")
print(f"Valid menurut corrected r ≥ 0,30        : {valid_rc} butir")

selisih = tabel_validitas.assign(Selisih=(tabel_validitas["r hitung"] - tabel_validitas["Corrected r"]).round(3))
rata_selisih = selisih.groupby("Dimensi", sort=False).agg(jumlah_butir=("Butir", "count"),
                                                         rata_selisih=("Selisih", "mean")).round(3)
rata_selisih

# %% [markdown]
# ## Latihan 3: Perbaikan instrumen
# Modul meminta membuang satu butir yang **tidak valid**, lalu menjalankan ulang analisis dan membandingkan α dimensi.
# Jika tidak ada butir yang tidak valid, tidak ada butir yang dibuang dan seluruh butir dipertahankan.

# %%
tidak_valid = tabel_validitas[tabel_validitas["Keterangan"] == "Tidak valid"]
if tidak_valid.empty:
    print("Tidak ada butir yang tidak valid, sehingga tidak ada butir yang dibuang.")
    print("Seluruh", len(tabel_validitas), "butir dipertahankan; α setiap dimensi tetap seperti Langkah 7.")
    display(tabel_reliabilitas)
else:
    buang = tidak_valid.sort_values("r hitung").iloc[0]
    kolom_buang = next(k for k, v in KODE.items() if v == buang["Butir"] and k in dimensi[buang["Dimensi"]])
    dimensi_baru = {k: [c for c in v if c != kolom_buang] for k, v in dimensi.items()}
    rel_sesudah, _ = uji_reliabilitas(num, dimensi_baru)
    print(f"Butir yang dibuang: {buang['Dimensi']} {buang['Butir']}")
    display(tabel_reliabilitas[["Dimensi", "Cronbach's alpha"]].merge(
        rel_sesudah[["Dimensi", "Cronbach's alpha", "Kategori"]], on="Dimensi", suffixes=(" sebelum", " sesudah")))

# %% [markdown]
# ## Latihan 4: Pengaruh ukuran sampel (subset acak 20 responden)

# %%
num20 = num.sample(20, random_state=1)
val20, r_tabel20 = uji_validitas(num20, dimensi)
rel20, _ = uji_reliabilitas(num20, dimensi)
print(f"n = {len(num)} -> r tabel {r_tabel:.3f} | butir valid {valid_r}")
print(f"n = 20  -> r tabel {r_tabel20:.3f} | butir valid {(val20['Keterangan'] == 'Valid').sum()}")
display(val20[val20["Keterangan"] == "Tidak valid"])
display(tabel_reliabilitas[["Dimensi", "Cronbach's alpha"]].merge(
    rel20[["Dimensi", "Cronbach's alpha", "Kategori"]], on="Dimensi", suffixes=(f" n={len(num)}", " n=20")))
