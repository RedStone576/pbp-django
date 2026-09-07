# Tugas 1

## Instalasi dan *Deployment*

### Requirements
- Python 3.14+
- pip
- Git
- Lulus DDP1

### Local Preview

Clone *repository* ini
```bash
git clone https://github.com/redstone576/pbp-django.git
cd pbp-django
```

Buat *virtual environment*
```bash
python -m venv .venv

# Untuk mesin Windows, cmd sebagai shell (saya gunakan bash sepertinya tidak bisa)
.venv\Scripts\activate

# Untuk mesin Unix
source .venv/bin/activate
```

*Install* dependensi
```bash
pip install -r requirements.txt
```

Jalankan server
```
python manage.py migrate # local development uses SQLite by default so...
python manage.py runserver
```

Lalu buka `http://127.0.0.1:8000/`.

### Deployment

*Production* menggunakan PostgreSQL, jadi buat *project* baru di PWS dan set enviroment variables untuk database dari ITF seperti berikut:
```
PRODUCTION=True

DB_NAME=<database-name>
DB_USER=<database-user>
DB_PASSWORD=<database-password>
DB_HOST=<database-host>
DB_PORT=<database-port>
SCHEMA=public
```

Saya siapkan GitHub Actions agar setiap commit pada `master` akan di-mirror ke PWS. Jadi *copy* git URL, username, dan password project PWS lalu set GitHub Actions Secrets berikut:
```
PWS_USERNAME
PWS_PASSWORD
```

Git URL hardcoded di `.github/workflows/push_pws.yml`

Lalu tinggal melakukan commit / merge di `master`
```bash
git add .
git commit -m "chore: deploy"
git push origin master
```

## Apa yang berubah setelah Tutorial 01

- saya tambahkan favicon
- saya ubah warna aksen yang semulanya oranye menjadi pink
- saya ubah tampilan `.photo-block` dengan pure css gradient
- saya tambahkan section `Projects` 

## *Review* dari pak Daya
- [X] Setup Github Action untuk auto-deploy  
- [ ] Buat hamburger menu karena navbar pada display mobile terlihat sesak  
- [ ] Tambahkan section `Skills` / `Experiences`  

## Tools

- Git: version control
- Github: remote repository hosting
- Github Gist: untuk preview `.md`
- [Lite XL](https://lite-xl.com/): code editor yang saya gunakan
- Helium: browser yang biasa saya gunakan ketika mengembangkan website
- Firefox: browser yang biasa saya gunakan untuk menjadi komparasi karena memiliki *engine* yang berbeda untuk me-render CSS
- Django: web framework untuk Python

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-1.html#pertanyaan-reflektif)

> 1.  Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat _static web_? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

Ya, saya gunakan element semantic seperti `<section>` dan `<article>` untuk memberikan struktur dan makna pada konten. Selain membuat HTML lebih terstruktur, hal ini bisa membantu a11y[^1] karena struktur dokumen lebih mudah dipahami oleh browser dan screen reader.

[^1]: a11y: accessibility; sempat disinggung pada kuliah PBP kelas E di hari Senin 31 Agustus. 


> 2.  Ketika Anda mengatur CSS Anda agar tetap _responsive_, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

Layar mobile terlalu kecil untuk display horizontal, sehingga saya gunakan media query untuk mengubah layout bila mendeteksi ukuran layar yang lebih kecil


> 3.  Website yang Anda buat saat ini adalah _static web_ murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

Karena static, konten harus diubah secara manual dan tidak bisa mengambil data secara dinamis. Pada iterasi berikutnya, saya ingin setup backend untuk me-return data proyek dkk. sehingga konten dapat diperbarui tanpa mengubah template secara langsung.

### AI Disclosure

Saya gunakan Claude Haiku 4.5 ketika mencoba debugging gunicorn di windows (tanpa WSL 🥶🥶🥶) tetapi ya... lumayan mengecewakan.[^2]

Singkatnya:
```diff
--- ALLOWED_HOSTS = ["localhost", "127.0.0.1", "https://username-portofolio.pws.cs.ui.ac.id"]
+++ ALLOWED_HOSTS = ["localhost", "127.0.0.1", "username-portofolio.pws.cs.ui.ac.id"]
```

Bisa ditebak karena Claude tidak memiliki konteks yang cukup akan PWS untuk melakukan debugging. Mungkin karena saya tidak jago vibe coding / the so called prompt "engineering," and i got zero interest in it.

[^2]: https://claude.ai/share/dde770f1-ddf5-407e-876d-bd7796a2e6f9

## Refrensi

- https://developer.mozilla.org/en-US/
