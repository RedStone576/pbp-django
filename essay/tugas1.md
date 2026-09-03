# Tugas 1

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-1.html#pertanyaan-reflektif)

> 1.  Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat _static web_? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Ya, saya gunakan element semantic seperti `<section>` dan `<article>` untuk memberikan struktur dan makna pada konten. Selain membuat HTML lebih terstruktur, hal ini bisa membantu a11y* karena struktur dokumen lebih mudah dipahami oleh browser dan screen reader.

*a11y: accessibility; sempat disinggung pada kuliah PBP kelas E di hari Senin 31 Agustus. 


> 2.  Ketika Anda mengatur CSS Anda agar tetap _responsive_, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Layar mobile terlalu kecil untuk display horizontal, sehingga saya gunakan media query untuk mengubah layout bila mendeteksi ukuran layar yang lebih kecil


> 3.  Website yang Anda buat saat ini adalah _static web_ murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Karena static, konten harus diubah secara manual dan tidak bisa mengambil data secara dinamis. Pada iterasi berikutnya, saya ingin setup backend untuk me-return data proyek dkk. sehingga konten dapat diperbarui tanpa mengubah template secara langsung.

## Tools

- Git: version control
- Github: remote repository hosting
- Lite XL: code editor yang saya gunakan
- Helium: browser yang biasa saya gunakan ketika mengembangkan website
- Firefox: browser yang biasa saya gunakan untuk menjadi komparasi karena memiliki *engine* yang berbeda untuk me-render CSS
- Django: web framework untuk Python


## Refrensi

- https://developer.mozilla.org/en-US/

### AI Disclosure

Saya gunakan Claude Haiku 4.5 ketika mencoba debugging gunicorn di windows (tanpa WSL 🥶🥶🥶) tetapi ya... lumayan mengecewakan.

### Special Thanks
- Mas "Bagas" Fossy (https://github.com/fossyy), karena merupakan devops terbaik.
- Pak Daya, karena merupakan dosen terbaik.
- Pacar saya, karena merupakan pacar terbaik.
- Manajemen Fakultas Ilmu Komputer, karena merupakan fakultas terbaik.
- Rektor Universitas Indonesia, karena merupakan universitas terbaik.
- Tim Asdos PBP, karena merupakan tim asdos terbaik.0

### Licnese
*to be added later*
