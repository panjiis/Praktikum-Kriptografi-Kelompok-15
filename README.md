# Projek UAS Kriptografi
program enkripsi password berdasarkan username menggunakan Affine Chipper dan Columnar Chipper

### anggota

- 140810220011 (Panji) 
- 140810220059 (Ilham)
- 1408102200 (jaya)

### Cara kerja Register

- memasukan `username` berupa angka dan `password` berupa huruf atau angka
- ambil 2 digit terakhir dari `username` untuk `b`, dan next primenya sebagai `a`
- gunakan affine chipper untuk mengenkripsinya dengan `a`, `b`, dan `p` = 36 (10 angka dan 26 huruf)
- ambil 4 digit terakhir `username` dan jadikan sebagai `key`
- enkripsikan hasil affine chipper dengan columnar chipper menggunakan `key` tadi
- masukan ke database

### Cara kerja Register

- memasukan `username` berupa angka dan `password` berupa huruf atau angka
- ambil `password` dari database
- ambil 4 digit terakhir npm dan jadikan sebagai `key`
- dekripsikan `password` dari database dengan columnar chipper menggunakan `key` tadi
- ambil 2 digit terakhir dari `username` untuk `b`, dan next primenya sebagai `a`
- gunakan affine chipper untuk mendeskripsikan `password` dari database dengan `a`, `b`, dan `p` = 36 (10 angka dan 26 huruf)
- pastikan hasil deskripsi `password` database sama dengan `password` yang diinput
