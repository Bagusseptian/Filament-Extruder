#!/usr/bin/env python3
"""
Pembuat kode QR untuk Pusat Dokumentasi Alat.

Cara pakai:
    python3 buat-qr.py "https://alamat-website-anda.com"
    python3 buat-qr.py "https://..." "Judul di poster"

Hasil tersimpan di folder qr/ :
    qr-code.png     -> untuk ditempel di slide / dokumen
    qr-code.svg     -> vektor, tidak pecah saat dicetak sebesar apa pun
    poster-qr.pdf   -> poster A4 siap cetak dan tempel di dekat alat

Tidak butuh internet dan tidak butuh pustaka tambahan.
"""

import os
import sys
import zlib
import struct

from reportlab.graphics.barcode import qr
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

QUIET = 4  # margin kosong wajib di sekeliling QR (satuan modul)


def buat_matriks(data, level="H"):
    """Menghasilkan matriks QR berupa list of list berisi True/False."""
    w = qr.QrCodeWidget(data, barLevel=level)
    w.getBounds()  # wajib dipanggil dulu agar matriks QR dibangun
    return [[bool(sel) for sel in baris] for baris in w.qr.modules]


def tulis_png(path, m, scale=20, fg=(0, 0, 0), bg=(255, 255, 255)):
    n = len(m)
    size = (n + 2 * QUIET) * scale
    baris_png = []
    for y in range(size):
        my = y // scale - QUIET
        row = bytearray()
        for x in range(size):
            mx = x // scale - QUIET
            hidup = 0 <= my < n and 0 <= mx < n and m[my][mx]
            row += bytes(fg if hidup else bg)
        baris_png.append(b"\x00" + bytes(row))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(b"".join(baris_png), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return size


def tulis_svg(path, m, scale=10):
    n = len(m)
    total = (n + 2 * QUIET) * scale
    bagian = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="{total}" '
        f'viewBox="0 0 {total} {total}" shape-rendering="crispEdges">',
        f'<rect width="{total}" height="{total}" fill="#ffffff"/>',
        '<g fill="#000000">',
    ]
    for y in range(n):
        x = 0
        while x < n:
            if m[y][x]:
                mulai = x
                while x < n and m[y][x]:
                    x += 1
                px = (mulai + QUIET) * scale
                py = (y + QUIET) * scale
                bagian.append(
                    f'<rect x="{px}" y="{py}" width="{(x - mulai) * scale}" '
                    f'height="{scale}"/>'
                )
            else:
                x += 1
    bagian.append("</g></svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(bagian))


def potong(c, teks, font, ukuran, lebar_maks):
    """Perkecil ukuran font sampai teks muat pada lebar tertentu."""
    while ukuran > 6 and c.stringWidth(teks, font, ukuran) > lebar_maks:
        ukuran -= 0.5
    return ukuran


def tulis_poster(path, m, url, judul, subjudul):
    W, H = A4
    c = canvas.Canvas(path, pagesize=A4)

    # latar putih penuh agar kontras QR maksimal saat dipindai
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # kop atas gelap bergaya teknik
    c.setFillColorRGB(0.09, 0.09, 0.09)
    c.rect(0, H - 122, W, 122, fill=1, stroke=0)
    for i, warna in enumerate([(0.37, 0.62, 0.91), (0.92, 0.76, 0.42),
                               (0.45, 0.74, 0.56), (0.91, 0.45, 0.40)]):
        c.setFillColorRGB(*warna)
        c.rect(i * W / 4, H - 128, W / 4, 6, fill=1, stroke=0)

    c.setFillColorRGB(1, 1, 1)
    uk = potong(c, judul, "Helvetica-Bold", 24, W - 112)
    c.setFont("Helvetica-Bold", uk)
    c.drawCentredString(W / 2, H - 72, judul)

    c.setFillColorRGB(0.75, 0.75, 0.75)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, H - 97, subjudul)

    # ajakan memindai
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(W / 2, H - 182, "PINDAI UNTUK MEMBUKA")

    c.setFillColorRGB(0.42, 0.42, 0.42)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(W / 2, H - 202,
                        "Arahkan kamera ponsel ke kode di bawah ini")

    # kode QR
    n = len(m)
    sisi = 300.0
    modul = sisi / n
    x0 = (W - sisi) / 2
    y0 = H - 246 - sisi

    pad = 18
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(1)
    c.roundRect(x0 - pad, y0 - pad, sisi + 2 * pad, sisi + 2 * pad,
                10, fill=1, stroke=1)

    c.setFillColorRGB(0, 0, 0)
    for y in range(n):
        x = 0
        while x < n:
            if m[y][x]:
                mulai = x
                while x < n and m[y][x]:
                    x += 1
                c.rect(x0 + mulai * modul,
                       y0 + (n - 1 - y) * modul,
                       (x - mulai) * modul, modul, fill=1, stroke=0)
            else:
                x += 1

    # alamat cadangan bila QR gagal dipindai
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, y0 - 52, "Atau ketik alamat berikut di peramban:")

    c.setFillColorRGB(0.12, 0.12, 0.12)
    uk = potong(c, url, "Courier-Bold", 11.5, W - 112)
    c.setFont("Courier-Bold", uk)
    c.drawCentredString(W / 2, y0 - 70, url)

    # daftar isi ringkas
    c.setStrokeColorRGB(0.88, 0.88, 0.88)
    c.line(90, y0 - 104, W - 90, y0 - 104)

    c.setFillColorRGB(0.30, 0.30, 0.30)
    c.setFont("Helvetica", 10.5)
    isi = "Buku Panduan  \u2022  Labsheet Praktikum  \u2022  Video Demonstrasi"
    c.drawCentredString(W / 2, y0 - 124, isi)

    # kaki halaman agar bobot visual seimbang dengan kop atas
    c.setFillColorRGB(0.09, 0.09, 0.09)
    c.rect(0, 0, W, 58, fill=1, stroke=0)
    for i, warna in enumerate([(0.37, 0.62, 0.91), (0.92, 0.76, 0.42),
                               (0.45, 0.74, 0.56), (0.91, 0.45, 0.40)]):
        c.setFillColorRGB(*warna)
        c.rect(i * W / 4, 58, W / 4, 6, fill=1, stroke=0)

    c.setFillColorRGB(0.68, 0.68, 0.68)
    c.setFont("Helvetica", 9.5)
    c.drawCentredString(W / 2, 25, "Pendidikan Teknik Mekatronika \u00b7 Universitas Negeri Yogyakarta")

    c.showPage()
    c.save()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1].strip()
    judul = sys.argv[2].strip() if len(sys.argv) > 2 else "Filament Ekstruder"
    subjudul = "Buku panduan, labsheet, dan video demonstrasi alat"

    keluar = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr")
    os.makedirs(keluar, exist_ok=True)

    m = buat_matriks(url, level="H")

    px = tulis_png(os.path.join(keluar, "qr-code.png"), m)
    tulis_svg(os.path.join(keluar, "qr-code.svg"), m)
    tulis_poster(os.path.join(keluar, "poster-qr.pdf"), m, url, judul, subjudul)

    print(f"Alamat   : {url}")
    print(f"Ukuran   : {len(m)}x{len(m)} modul, koreksi galat tingkat H (30%)")
    print(f"Tersimpan di folder qr/")
    print(f"  qr-code.png    ({px}x{px} piksel)")
    print(f"  qr-code.svg    (vektor)")
    print(f"  poster-qr.pdf  (A4 siap cetak)")


if __name__ == "__main__":
    main()
