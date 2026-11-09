# Tugas 6

## Requirements
- Tugas 5
- Tutorial 7
- Pernah self-host PWS ketika PWS sedang down

## TL;DR
- clean up kode dari Tutorial 7
- Menyatukan handler education, experience, dan projects (but make it generic yo)
- Menerapkan permission owner, editor, visitor, dan pengunjung
- search, add, edit, stars (or bloom :3), dan delete data tanpa reload

## Checklist

- [X] Serializer:
    - [X] Membuat ModelSerializer untuk model bagianmu di main/serializers.py, dengan daftar fields yang ditulis eksplisit (bukan "__all__").
    - [X] Menyertakan informasi star dari Tugas 4 sebagai field hasil perhitungan yang bersifat read-only, minimal jumlah star dan status star pengguna yang sedang login. Data akun sensitif, seperti email atau password hash, tidak boleh ikut tampil.
    - [X] Memvalidasi input teks di method validate_<field>, termasuk membersihkannya dengan strip_tags seperti clean_<field> pada Tugas 5.
- [X] Permission:
    - [X] Menerapkan IsPortfolioOwnerOrEditorOrReadOnly dari Tutorial 07 (atau permission class lain yang setara) pada endpoint daftar dan detail bagianmu, sesuai keempat peran di atas.
    - [X] Memakai IsAuthenticated pada endpoint star, dengan akun pemberi star selalu diambil dari request.user.
- [X] API View dan URL:
    - [X] Membuat API view berbasis fungsi dengan @api_view dan SessionAuthentication di main/api_views.py untuk daftar (GET, POST), detail (GET, PUT, PATCH, DELETE), dan star (POST).
    - [X] Memindahkan pencarian dari Tugas 5 ke parameter query pada endpoint daftar.
    - [X] Mengembalikan status HTTP yang sesuai: 201 saat data dibuat, 400 untuk input yang tidak valid, 403 untuk tindakan yang tidak diizinkan, 404 untuk data yang tidak ditemukan, dan 204 setelah data dihapus.
    - [X] Mendaftarkan endpoint bagianmu di main/api_urls.py di bawah prefix /api/v1/ yang sama dengan API dari Tutorial 07 (misalnya /api/v1/education/), dengan nama URL yang unik.
- [X] Integrasi Halaman:
    - [X] Mengubah halaman bagianmu dari Tugas 5 agar menampilkan, mencari, menambah, memberi star, dan menghapus data lewat API baru tanpa me-reload halaman.
    - [X] Menyediakan cara mengubah data dari halaman tersebut lewat PUT atau PATCH ke API (misalnya modal edit baru, atau halaman edit dari Tugas 3 yang diubah agar mengirim data lewat fetch()), yang dapat dipakai oleh Editor dan pemilik portofolio.
    - [X] Menampilkan pesan kesalahan dari API (validasi 400 dan penolakan 403) lewat toast.
    - [X] Menyertakan header X-CSRFToken pada setiap permintaan yang mengubah data, serta tetap melakukan escaping pada setiap nilai teks yang disisipkan ke HTML.
- [X]Testing:
    - [X] Menulis test dengan APITestCase untuk bagianmu yang mencakup setiap peran: pengunjung dan pengguna biasa ditolak saat menulis data, Editor dapat melakukan PATCH tetapi ditolak saat membuat dan menghapus data, serta pemilik dapat membuat dan menghapus data.
    - [X] Memeriksa isi database pada test penolakan, bukan hanya status HTTP-nya.
    - [X] Menulis test untuk validasi input dan untuk star, termasuk penolakan bagi pengunjung tanpa login.
    - [X] Menulis minimal satu test dengan APIClient(enforce_csrf_checks=True) dan .login() yang membuktikan permintaan tanpa token CSRF ditolak.
- [X] Eksekusi:
    - [X] Memastikan python manage.py test main lulus, termasuk test dari Tutorial 07.
    - [X] Memastikan proyek berjalan tanpa error dengan python manage.py runserver, Browsable API untuk endpoint bagianmu dapat dibuka, dan halaman dari Tutorial 07 tetap berfungsi.

## Pertanyaan

> 1. Jelaskan apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful! Jelaskan pula perbedaan `PUT` dan `PATCH` beserta contoh kapan masing-masing sebaiknya digunakan!

REST adalah style arsitektur API yang menggunakan HTTP method untuk mengakses dan mengelola resource. Tapi ya JSON saja belum cukup karena API juga harus mengikuti prinsip REST, seperti stateless dan penggunaan HTTP method yang sesuai.

Dan,
- `PUT`: mengganti seluruh data resource.
- `PATCH`: mengganti sebagian data resource.

> 2. Jelaskan peran serializer pada Django REST Framework! Apa keuntungannya dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05?

Serializer berfungsi untuk mengubah data model Django menjadi JSON atau sebaliknya. Dibandingkan JsonResponse dengan "merakit" dictionary manual, serializer menyediakan validasi otomatis, clean code, dan *reusability*.

> 3. Jelaskan perbedaan autentikasi dan otorisasi pada Django REST Framework! Mengapa hak akses harus diperiksa dengan *permission class* di server, bukan hanya dengan menyembunyikan tombol di template?

- Autentikasi: memeriksa identitas pengguna.
- Otorisasi: memeriksa hak akses pengguna.

Permission class diperlukan di server karena menyembunyikan button pada template saja tidak mencegah pengguna mengirim request secara langsung melalui layer network (dengan CURL dan kawan-kawan misal).

> 4. Jelaskan mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai `SessionAuthentication`! Mengapa test yang memakai `force_authenticate` tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?

Ya karena `SessionAuthentication` menggunakan session cookie yang dikirim browser itu sendiri. Token CSRF diperlukan untuk memastikan request yang mengganti data bukan berasal dari website lain yang sedang cosplay user tersebut dengan session mereka.

Lalu, `force_authenticate` tidak cukup untuk menge-test CSRF karena melewati proses autentikasi yang biasa(?). Pengujian CSRF sebaiknya dengan `enforce_csrf_checks=True`.

## Referensi, seperti biasa:

- https://developer.mozilla.org/en-US/
- https://docs.djangoproject.com/en/5.0/
- https://www.django-rest-framework.org/ (NEW!!!)

## Artificial Intelligence Disclosure

Okay check this out https://0rwx.com/, menurut saya menarik ya. 

TL;DR, ada 4 level dalam framework tersebut: 
- 0 (Zero): "Tidak ada AI yang digunakan"
- R (Read): "Saya yang menulis kodenya"
- W (Write) "Saya yang me-review kodenya"
- X (Execute) "Saya yang mengkurasi kodenya," atau dalam kata lain: "saya full vibe coding" awoawkwaokwa

Label-label tersebut terinspirasi dari permission di sistem Unix btw. I use Fedora btw.

Semoga dapat berguna.

Ada bagian di mana saya menggunakan Codex untuk meng-audit, ada juga bagian di mana saya membuat Codex untuk menulis kode.

- AI:0
    - none
- AI:R
    - `assignment6.txt`
    - `tutorial-7.pdf`
    - `main/models.py`
    - `main/forms.py`
    - `main/views/pages.py`
    - `main/views/utils.py`
    - `main/tests/test_api_projects.py`
    - `templates/layouts/form_modal.html`
    - `templates/layouts/edit_modal.html`
    - `main/api/permissions.py`
    - `main/api/serializers/common.py`
    - `main/api/serializers/education.py`
    - `main/api/serializers/experience.py`
    - `main/api/serializers/projects.py`
    - `main/api/urls.py`
    - `main/urls.py`
    - `main/api/views/__init__.py`
    - `main/views/__init__.py`
- AI:W
    - `main/test_api_resources.py`
    - `main/tests/test_views.py`
    - `static/ts/fetch_list.ts`
    - `static/ts/list.ts`
    - `templates/main/education.html`
    - `templates/main/experience.html`
    - `templates/main/projects.html`
- AI:X (yeah i dont like unit testing)
    - `main/test_api_resources.py`
    - `main/tests/test_api_projects.py`
    - `main/tests/test_models.py`
    - `main/tests/test_serializers.py`
    - `main/tests/test_views.py`

