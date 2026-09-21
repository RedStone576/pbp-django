# Tugas 3

### Requirements
- Tugas 2
- Tutorial 3

## TL;DR
- buat _shared skeleton structure_(?) `templates/base.html`
- buat `ModelForm` baru
- implement CRUD tentunya
- buat UI untuk create, edit, dan delete

## Checklist
- [X] Setiap berkas html yang identik di-refactor dengan melakukan extend dari root html template
- [X] Buat ModelForm baru di berkas forms.py aplikasi main yang merepresentasikan form data pilihanmu dengan minimal 3 (tiga) buah field selain id dan timestamp dengan tipe data yang bervariasi
- [X] Definisi kelas ModelForm baru tersebut memiliki setiap field data yang dapat kamu isi, kecuali field seperti id atau yang berhubungan dengan timestamp
- [X] Buat fungsi view untuk bagian yang dipilih:
    - [X] Create data menggunakan form
    - [X] Update data menggunakan form
    - [X] Delete data
    - [X] Mengambil data dalam format JSON
    - [ ] Menampilkan data setelah mengambil JSON dan melakukan deserialisasi
- [X] Pastikan data pada bagian yang kamu pilih dapat tampil di halaman web dengan baik
- [X] Buat antarmuka untuk bagian yang dipilih:
    - [X] Halaman/form create data
    - [X] Halaman/form update data
    - [X] Tombol delete yang terhubung ke fungsi view delete data
- [X] Pastikan proyek dapat dijalankan dengan python manage.py runserver tanpa error

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-2.html#pertanyaan-reflektif)
> 1.  Jelaskan mengapa kita menggunakan `ModelForm` pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!

Agar modular dan tidak hardcoded.

> 2.  Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

Ya karena lebih sederhana, lebih human-readabke, dan lebih storage/bandwidth-efficient.

> 3.  Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

Jadi, _something like this:_

```
Browser fetch -> URL return -> View return -> Model return -> Serialization return -> JSON Response return -> Kembali ke browser
```

Butuh _serialization_ karena _Django object_ tidak bisa dikirim langsung melalui HTTP, perlu diformat menjadi JSON (atau bila anda bosan, menjadi XML) terlebih dahulu.

### AI Disclosure

Tidak ada LLM yang digunakan. 

## Referensi

- https://developer.mozilla.org/en-US/
