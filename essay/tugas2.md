# Tugas 2

<img width="1366" height="422" alt="image" src="https://github.com/user-attachments/assets/b57f8442-e436-44a6-948b-9f181b6e0758" />

### Requirements
- [Tugas 1](https://github.com/RedStone576/pbp-django/releases/tag/1.4.1)
- [Tutorial 2](https://github.com/RedStone576/pbp-django/releases/tag/1.5.0)

## Credits
- [@faeiz-ff](https://github.com/faeiz-ff) - https://faeiz-faiza-myportofolio.pws.cs.ui.ac.id/
- [@fossyy](https://github.com/fossyy) - https://bagas-aulia-myportofolio.pws.cs.ui.ac.id/

## TL;DR

- meniru desain https://firmansyah.cesilia.dev (my own website btw)
- new routes: `/experience/`, `/education/`, dan `projects/` 
- mengaktivasi admin panel untuk editing enteri database, saya buatkan guide untuk rekan-rekan mahasiswa juga:   
https://gist.github.com/RedStone576/90f5eb53acae3bc668d2ef3ea9205e3c
- membuat Conway's Game of Life varian "immigration" dengan warna lucuuuuu sebagai background website
- "Sistem Informasi" -> "06.00.12.01" agar terlihat teknis :3
- downgrade versi Django ke 5.0.

## TODO
- [ ] figure out how state works in django, karena setiap berganti halaman, background Game of Life saya kembali ke initial state.

## [Pertanyaan Reflektif](https://pbp.cs.ui.ac.id/assignments/individual/tugas-2.html#pertanyaan-reflektif)

> 1.  Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran `urls.py` proyek, `urls.py` aplikasi, view, model, dan template.

```
GET /education/ -> urls.py route ke show_education() view -> view query Education.objects.all() -> pass data ke template -> template render HTML -> browser display.
```

- `urls.py` project: router ke app
- `urls.py` app: match route, panggil view
- View: query model, pass ke template
- Model: mendefinisikan schema dan querying(?) database
- Template: me-render data menjadi HTML

> 2.  Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

Karena bila hardcoded, akan sulit untuk mengubah HTML-nya dan tidak modular. 

> 3.  Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

`makemigrations` Generates `.py` "migration files" dari perubahan model. Sedangkan `migrate` lah yang akan menjalankan migration files tersebut dan mengupdate _fields_ database.

### AI Disclosure

Tidak ada LLM yang digunakan. Welcome to our recreational programming session >:3

## Referensi

- https://developer.mozilla.org/en-US/
- https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
- https://rustwasm.github.io/book/game-of-life/rules.html
- https://gitosthenes.github.io/Immigration_Automata/
