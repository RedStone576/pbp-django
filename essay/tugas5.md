# Tugas 5

## Requirements
- Tugas 4
- Tutorial 5
- Lulus DDP2

## TL;DR
- Migrate SSR menjadi SPA. 
- Pencarian menggunakan teknik _debouncing_
- penambahan/edit data dilakukan melalui *popover modal* yang hotreloaded(?) 
- anti XSS di frontend dan backend (checkout this cool custom decorator `@strip_html_tags`)
- menambahkan states (loading, error, empty) pada skeleton(?) fetch list

## Checklist

- [X] Menampilkan Data dengan AJAX:
    - [X] Mengubah halaman daftar agar hanya merender kerangka halaman, lalu mengambil data dari endpoint JSON menggunakan fetch().
    - [X] Menyusun respons JSON secara manual dengan JsonResponse, termasuk informasi star dari Tugas 4 (jumlah star dan status star pengguna yang sedang login).
    - [X] Menampilkan kondisi loading saat data dimuat, kondisi data kosong, dan kondisi error saat data gagal dimuat.
- [X] Pencarian dengan Debouncing:
    - [X] Menyediakan pencarian lewat AJAX berdasarkan minimal satu field tanpa me-reload halaman.
    - [X] Menerapkan debouncing sehingga permintaan hanya dikirim setelah pengguna berhenti mengetik.
- [X] Menambahkan Data dengan Modal dan AJAX:
    - [X] Menampilkan form tambah data di dalam modal pada halaman daftar, bukan di halaman terpisah.
    - [X] Membuat view POST yang memvalidasi input dengan ModelForm dan membalas dengan JSON beserta status HTTP yang sesuai (201, 400, 403).
    - [X] Memeriksa hak akses di dalam view sesuai peran dari Tugas 4, bukan hanya menyembunyikan tombol di template.
    - [X] Menyertakan token CSRF pada permintaan POST, melalui field csrfmiddlewaretoken dari {% csrf_token %} atau header X-CSRFToken.
    - [X] Memperbarui daftar data tanpa me-reload halaman setelah data berhasil ditambahkan.
- [X] Notifikasi Toast:
    - [X] Menampilkan toast saat data berhasil ditambahkan dan saat terjadi kegagalan, termasuk pesan kesalahan validasi dari server.
- [X] Perlindungan XSS:
    - [X] Melakukan escaping pada setiap nilai teks yang disisipkan ke HTML melalui JavaScript (misalnya dengan escapeHtml atau textContent).
    - [X] Membersihkan input teks di sisi server menggunakan strip_tags pada method clean_<field> di ModelForm.
    
## Pertanyaan

> 1. Jelaskan apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX!

Debouncing adalah teknik untuk "menunda" eksekusi sebuah function hingga terlah berlalu waktu tertentu sejak event terakhir ter-_emit_. _Basically_, agar browser tidak melakukan *spam* request ke server setiap kali kita mengetik satu huruf pada _search query_. Jadi request hanya akan dikirim setelah kita benar-benar selesai mengetik, yang sangat menghemat *bandwidth* dan beban backend.

> 2. Jelaskan fungsi dari penggunaan `await` ketika kita menggunakan `fetch()`! Apa yang akan terjadi jika kita tidak menggunakan `await`?

`fetch()` merupakan operasi _asynchronous_, jadi hasilnya tidak langsung tersedia. `fetch()` mengembalikan sebuah `Promise` yang nantinya akan diselesaikan ketika request selesai. And then `await` digunakan untuk menunggu `Promise` itu selesai sebelum melanjutkan eksekusi kode di dalam _asynchronous function_.

Dengan `await`:
```js
const response = await fetch("/api/jawa)"
const data     = await response.json()

console.log(data)
```

tanpa `await`:
```js
const response = fetch("/api/jawa")

console.log(response) // returns Promise<Response>
```

perlu melakukan `.then(x => (...))` pada `response`.

> 3. Jelaskan apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django!

XSS (Cross-Site Scripting) adalah serangan dengan memasukkan code JavaScript "berbahaya" ke dalam halaman web. Data yang ditampilkan melalui AJAX/JavaScript lebih berisiko jika langsung dimasukkan ke HTML menggunakan innerHTML, karena input tersebut bisa dianggap sebagai kode HTML/JavaScript lalu dieksekusi oleh browser.

## Referensi (yah standar lah)

- https://developer.mozilla.org/en-US/
- https://docs.djangoproject.com/en/5.0/

## Human Intelligence Disclosure
- [@faeiz-ff](https://github.com/faeiz-ff) - https://faeiz-faiza-myportofolio.pws.cs.ui.ac.id/
- [@fossyy](https://github.com/fossyy) - https://bagas-aulia-myportofolio.pws.cs.ui.ac.id/

## Artificial Intelligence Disclosure

Tidak ada LLM / GenAI yang digunakan.
