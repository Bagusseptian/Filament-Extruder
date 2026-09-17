# Filament Ekstruder — Website Dokumentasi

Program Studi Pendidikan Teknik Mekatronika
Departemen Pendidikan Teknik Elektro, Universitas Negeri Yogyakarta

Website statis satu halaman berisi buku panduan (flipbook), tiga labsheet (flipbook),
dan video demonstrasi alat. Tidak butuh server khusus, tidak butuh database.

Buku panduan dan seluruh labsheet dibaca langsung dari Heyzine, jadi **tidak ada berkas PDF
yang perlu diunggah**. Yang tersisa hanyalah berkas video.

## Struktur folder

```
situs-alat/
├── index.html          <- seluruh website ada di sini
├── assets/
│   ├── logo-uny.png    <- logo UNY (navbar, hero, footer, favicon)
│   └── animasi-poster.png  <- sampul animasi (berlatar transparan)
├── models/
│   └── alat.glb         <- model 3D alat (bisa diputar dengan mouse/sentuh)
├── videos/
│   ├── animasi-desain.webm <- animasi berlatar transparan (utama)
│   ├── animasi-desain.mp4  <- cadangan untuk Safari (latar putih)
│   └── demonstrasi-alat.mp4  <- taruh video demonstrasi di sini (belum ada)
├── buat-qr.py          <- pembuat kode QR + poster A4
└── qr/                 <- hasil kode QR
```

## Cara mengganti isi

Buka `index.html`, cari blok `const CONFIG = {` di bagian bawah file. Semua isi website
diatur dari situ — tidak perlu menyentuh bagian lain.

```js
const CONFIG = {
  namaAlat: "Filament Ekstruder",
  penyusun: "Farrel Argya Hafizh",

  institusi: {
    universitas: "Universitas Negeri Yogyakarta",
    departemen: "Departemen Pendidikan Teknik Elektro",
    prodi: "Program Studi Pendidikan Teknik Mekatronika"
  },

  bukuPanduan: {
    judul: "Buku Panduan Penggunaan Alat",
    flipbook: "https://heyzine.com/flip-book/011539811c.html",  // link Heyzine
    file: ""                                                    // kosong = tombol unduh hilang
  },

  labsheets: [
    { no:"LS-01", judul:"Labsheet 1", desc:"Keterangan singkat.",
      flipbook:"https://heyzine.com/flip-book/36f10b3989.html", warna:"blue" },
    { no:"LS-02", judul:"Labsheet 2", desc:"Keterangan singkat.",
      flipbook:"https://heyzine.com/flip-book/ec938d4181.html", warna:"yellow" },
    { no:"LS-03", judul:"Labsheet 3", desc:"Keterangan singkat.",
      flipbook:"https://heyzine.com/flip-book/9f4cccb2d5.html", warna:"green" }
  ],

  videos: [
    { judul:"Demonstrasi Pengoperasian Alat", desc:"Keterangan.", durasi:"",
      type:"file", src:"videos/demonstrasi-alat.mp4", warna:"green" }
  ]
};
```

### Labsheet tampil sebagai tab

Seluruh labsheet berbagi satu penampil flipbook. Setiap baris di `CONFIG.labsheets`
menjadi satu tombol tab di atas penampil; menekan tab akan mengganti isi flipbook
tanpa memuat ulang halaman.

Menambah labsheet keempat cukup dengan menyalin satu baris `{ ... }`. Jumlah tab dan
angka statistik di bagian atas ikut menyesuaikan otomatis.

### Tampilan video menyesuaikan jumlah berkas

| Jumlah video | Tampilan |
| --- | --- |
| Satu | Pemutar besar 16:9, diputar langsung di halaman |
| Dua atau lebih | Grid thumbnail, video terbuka di popup |

Kolom `durasi` boleh dikosongkan (`""`); labelnya akan disembunyikan.

**Pilihan `warna`:** `blue`, `yellow`, `green`, `pink`, `red`.

**Dua jenis video:**

| type | src diisi dengan | contoh |
| --- | --- | --- |
| `"file"` | path video lokal | `"videos/01-pengenalan.mp4"` |
| `"youtube"` | link YouTube apa pun | `"https://youtu.be/xxxxxxxxxxx"` |

Menambah jobsheet atau video cukup dengan menyalin satu baris `{ ... }` lalu
menambahkannya ke dalam daftar. Angka statistik di bagian atas ikut terhitung otomatis.

## Flipbook Heyzine

Buku panduan tampil sebagai **flipbook interaktif** yang disematkan langsung dari Heyzine,
lengkap dengan animasi membalik halaman. Pembaca tidak perlu meninggalkan website.

Tiga tombol tersedia di atas flipbook:

| Tombol | Fungsi |
| --- | --- |
| Layar Penuh | Memperbesar flipbook memenuhi layar (tekan `Esc` untuk keluar) |
| Tab Baru | Membuka flipbook di halaman Heyzine aslinya |

**Mengganti bukunya:** unggah PDF baru ke Heyzine, salin link flip-book-nya,
lalu tempelkan ke `CONFIG.bukuPanduan.flipbook`. Cara yang sama berlaku untuk labsheet.

**Ingin tombol unduh PDF muncul kembali?** Buat folder `files/`, taruh PDF-nya di sana,
lalu isi `CONFIG.bukuPanduan.file` dengan path-nya, misalnya `"files/buku-panduan.pdf"`.

Catatan: flipbook dimuat dari server Heyzine, jadi butuh koneksi internet.
Bila gagal dimuat, halaman menampilkan pesan beserta tombol cadangan.

## Kode QR

Jalankan skrip `buat-qr.py` dengan alamat website Anda:

```bash
cd situs-alat
python3 buat-qr.py "https://alamat-website-anda.com"
```

Ingin judul poster yang berbeda? Tambahkan sebagai argumen kedua:

```bash
python3 buat-qr.py "https://..." "Trainer Kit Sistem Kendali"
```

Hasilnya tersimpan di folder `qr/`:

| Berkas | Kegunaan |
| --- | --- |
| `qr-code.png` | 980 × 980 piksel, untuk slide presentasi atau dokumen |
| `qr-code.svg` | Vektor, tetap tajam dicetak sebesar apa pun (banner, stiker) |
| `poster-qr.pdf` | Poster A4 siap cetak, tempel di dekat alat |

Skrip ini tidak butuh internet dan tidak butuh pustaka tambahan.
Bila alamat website berubah, jalankan ulang saja — berkas lama akan ditimpa.

**Catatan teknis:** QR dibuat dengan koreksi galat tingkat H (30%), artinya kode
tetap terbaca walau sebagian permukaannya kotor, tergores, atau tertutup logo kecil.

**Agar mudah dipindai saat dicetak:**

- Ukuran minimal sekitar 3 × 3 cm untuk jarak baca setengah meter
- Sisakan area putih di sekeliling kode, jangan dipepetkan ke tepi kertas
- Hindari mencetak di atas permukaan mengkilap yang memantulkan cahaya
- Jangan mengubah warna kode menjadi terang di atas latar gelap

## Cara menjalankan

**Lokal (uji coba):** klik dua kali `index.html`.
Sebagian peramban membatasi file lokal, jadi lebih baik jalankan server kecil:

```bash
cd situs-alat
python3 -m http.server 8000
# buka http://localhost:8000
```

**Online (hosting gratis):**

- **Netlify Drop** — buka app.netlify.com/drop, seret folder `situs-alat`. Selesai.
- **GitHub Pages** — unggah folder ke repositori, aktifkan Pages di Settings.
- **Vercel** — `vercel deploy` di dalam folder.

## Catatan tentang ukuran video

Hosting gratis biasanya membatasi ukuran file. Jika video Anda besar (di atas ~50 MB),
lebih aman diunggah ke YouTube (bisa disetel *Unlisted*) lalu pakai `type:"youtube"`.
Halaman tetap terlihat sama, hanya sumber videonya yang berbeda.

## Fitur yang sudah ada

- Tampilan gelap bergaya teknik industri dengan aksen warna per kategori
- Responsif di desktop dan ponsel, lengkap dengan menu geser
- Flipbook Heyzine tersemat dengan animasi balik halaman + mode layar penuh
- Pemutar video dalam popup (tekan `Esc` untuk menutup)
- Navigasi keyboard dan kontras teks sesuai standar aksesibilitas WCAG AA
