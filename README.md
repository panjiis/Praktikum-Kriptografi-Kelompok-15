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
### contoh input dan output

**input** : String `namaFile`

UAS_4.txt : 
```
95 95 92 100 Urawa Hanako 12 
88 85 80 90 Misono Mika 12 
59 42 55 50 Shirazu Azusa 11 
10 50 25 40 Asuma Toki 11 
99 100 100 97 Ushio Noa 11 
60 60 50 49 Sunaookami Shiroko 11 
50 23 51 31 Yutori Natsu 10 
34 56 60 13 Tsukiyuki Miyako 10 
52 14 25 42 Hakari Miyako 10 
60 20 40 32 Shimoe Koharu 10
```
input 1 : 
```
UAS_4.txt
```
output 1 : 
```
data mahasiswa kelas 10
semuanya remedial

data mahasiswa kelas 11
1) Ushio Noa : 98.7
Hanya 1 yang diatas KKM

data mahasiswa kelas 12
1) Urawa Hanako : 96.1
2) Misono Mika : 85.8
```
