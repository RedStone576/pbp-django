# Tugas 4

## Requirements
- Tugas 3
- Tutorial 4
- Lulus DDP2

## TL;DR 
- [Tutorial 4](https://github.com/RedStone576/pbp-django/compare/6cdcdb5675011f586f82d511bc31c477cfa6a3bd...ecc643da0d01176bea2d863b49e0d896aca00ff3):
    - membangun flow autentikasi
    - mengimplementasi otorisasi user.
    - _project starring_, di codebase saya namai "flower," dengan "bloom it"/"prune it" untuk star/unstar. Agar ada temanya saja sih.
- [Tugas 4](https://github.com/RedStone576/pbp-django/compare/ecc643da0d01176bea2d863b49e0d896aca00ff3...9cb75d00ead7a88b27e143d2febf0164590336fb):
    - memodelkan 4 roles user (user tidak terdaftar, user terdaftar, editor, dan superuser/owner)
    - membuat _secure API endpoint_.
- [_Beyond_ tugas 4](https://github.com/RedStone576/pbp-django/compare/9cb75d00ead7a88b27e143d2febf0164590336fb...666b47c682270c6928af8f7ac64fc8eb86a44b7e):
    - decouple `./main/views.py` yang monolitik parah menjadi modul-modul yang modularitasnya modular.
    - mengorganisasikan `./templates/` agar lebih intuitif
    - (akhirnya) setup linter, menggunakan Ruff di sini
    - setup `./AGENTS.md`
    - setup TypeScript.

## Checklist Tugas 4
- [X] Manajemen Hak Akses & Peran (Authorization):
    - [X] Menerapkan peran Editor melalui Django Group atau Permission (ditetapkan via Django Admin).
    - [X] Menerapkan pembatasan hak akses di sisi server (server-side check) sesuai 4 peran di atas (redirect ke login untuk pengunjung tanpa login; HTTP 403 Forbidden untuk aksi yang tidak diizinkan).
    - [X] Menyembunyikan tombol/kontrol aksi (create, update, delete) pada template bagi pengguna yang tidak berhak.
- [X] Fitur Interaktif Pemberian Star:
    - [X] Menambahkan relasi ManyToManyField ke model User pada model bagian portofolio pilihanmu dan menerapkan migrasi database.
    - [X] Mengimplementasikan view toggle_star (POST & {% csrf_token %}) untuk memberi/membatalkan star (maksimal satu star per pengguna) serta menampilkan jumlah total star dan status pengguna.
- [X] Integritas API & Keamanan Data:
    - [X] Memastikan endpoint JSON dari Tugas 3 tetap berfungsi tanpa membocorkan informasi sensitif.
- [X] Eksekusi:
    - [X] Memastikan proyek dapat dijalankan dengan python manage.py runserver tanpa error.

## Setup

Clone _repository_ ini
```sh
git clone https://github.com/redstone576/pbp-django.git
cd pbp-django
```

atau, pull commit baru ke local
```sh
git switch master
git fetch origin master
git pull origin master
```

Masuk ke Virtual Enviroment
```sh
# Untuk mesin Windows
.venv\Scripts\activate

# Untuk mesin Unix
source .venv/bin/activate
```

Lakukan _migration_ terlebih dahulu.
```sh
python manage.py makemigrations
python manage.py migrate
```

Install Ruff sebagai linter dan formater
```sh
pip install ruff
```

Lakukan formatting dan linting
```sh
ruff check --fix
```

Install TypeScript sebagai local dependency untuk frontend JavaScript
```sh
npm install -D typescript
```

Transpile TypeScript ke JavaScript
```
tsc --strict --noEmit true
```

Check semua baik-baik saja dan server bisa berjalan
```sh
python manage.py check
python manage.py runserver
``` 

## Referensi

- https://developer.mozilla.org/en-US/
- https://docs.djangoproject.com/en/5.0/
- https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-TEMPLATES-DIRS
- https://docs.astral.sh/ruff/
- https://www.typescriptlang.org/docs/
- https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes-oop.html
- https://www.typescriptlang.org/docs/handbook/typescript-tooling-in-5-minutes.html
- https://dev.to/suraj_khaitan_f893c243958/inside-google-antigravity-how-ai-pair-programming-actually-works-16nc

## Human Intelligence Disclosure
- [@faeiz-ff](https://github.com/faeiz-ff) - https://faeiz-faiza-myportofolio.pws.cs.ui.ac.id/
- [@fossyy](https://github.com/fossyy) - https://bagas-aulia-myportofolio.pws.cs.ui.ac.id/

## Artificial Intelligence Disclosure

Tidak ada LLM / GenAI yang digunakan dari sesi "Tutorial 4" hingga setup linter pada sesi "_Beyond_ tugas 4". Welcome again, to my recreational programming session :3

Jadi, ada apa dengan `AGENTS.md` tersebut? Mungkin sudah sekitar 7 tahun saya menjuluki diri sendiri sebagai seorang pemrogram komputer, ada sebuah _pride_ ketika menulis kode dengan tangan sendiri.
Namun, saya menyadari zaman akan berkembang, dan _inevitably_ juga _software engineering_, terutama _web development_.

Sehingga, saya rasa, _well, why not?_ Teman saya yang merupakan __**_DEVOPS RIZZTEK WEBDEV_**__ juga menggunakan _agentic AI coding tools_. 

_So i want to see whats all the hype is about._

Saya menggunakan Google Antigravity dengan model Gemini-3.1 Pro dengan skill Ponytail untuk melakukan audit dari keseluruhan codebase.

Lalu saya buat `AGENTS.md` yang merupakan _fork_ dari [pbp-fasilkom-ui/ai-debugging-example](https://github.com/pbp-fasilkom-ui/ai-debugging-example). Saya beri persona Burhan-chan, saya buat se-_cringe_ dan semalas mungkin dalam upaya mengurangi _brainrot_ dan ketergantungan berlebih. Saya contoh _setup_ tersebut dari _setup_ Ai-chan (Antigravity-chan)-nya pak Daya awokawokawokawoakw.

_Anyway_, saya minta Burhan-chan untuk memberi _walkthrough_ dalam meng-install TypeScript untuk frontend JavaScript di kemudian hari dan rewrite `static/js/life.js` (Conway's Game of Life with the "Immigration" rule).

Berikut isi percakapnnya, get ready for cringe:

```
> hi burhan-chan, please learn this codebase okay

▸ Thought for 5s, 334 tokens
  I'm now investigating the codebase structure. I'm using `run_command` to list the contents of the directory. My initial hunch is confirmed; it's...

● Bash(Get-ChildItem -Force | Select-Object Name, Length, LastWriteTime) (ctrl+o to expand)

▸ Thought for 3s, 19 tokens
  I've moved the processing task to the background for now. My current status is simply waiting for it to complete. I'll provide notification once...

▸ Thought for 5s, 354 tokens
  I'm focusing intently on tool specificity. I've been refining my approach to avoid unnecessary use of bash commands for file manipulation. I'm n...

● Read(~/programming/pbp-porto/requirements.txt)
● Read(~/programming/pbp-porto/readme.md) (ctrl+o to expand)
▸ Thought for 4s, 410 tokens
  I'm now prioritizing explicit tool listing before execution, thanks to my critical instruction! I'm dissecting tasks to identify all relevant to...

● Read(~/programming/pbp-porto/porto/settings.py)
● Read(~/programming/pbp-porto/main/models.py)
● Read(~/programming/pbp-porto/main/views.py) (ctrl+o to expand)
▸ Thought for 4s, 329 tokens
  I'm focusing intently on tool specificity. I've been refining my approach to avoid unnecessary `cat` usage for file creation or appending. Furth...

● Bash(Get-ChildItem -Path C:\Users\Cecilia\programming\pbp-porto\main -Force | Select-Object Name)
● Read(~/programming/pbp-porto/porto/urls.py)
● Bash(Get-ChildItem -Path C:\Users\Cecilia\programming\pbp-porto\main\views -Force | Select-Object Name) (ctrl+o to expand)

▸ Thought for 6s, 267 tokens
  I've grasped the project structure. It's a Django project, and I see `main` as the main application with a `views` package. The user is telling...

● Read(~/programming/pbp-porto/main/views/pages.py)
● Read(~/programming/pbp-porto/main/views/api.py)
● Read(~/programming/pbp-porto/main/views/crud.py) (ctrl+o to expand)
▸ Thought for 7s
  I'm now deep-diving into the `api.py` file. I found the use of `use_natural_foreign_keys=True` combined with `Model.objects.all()` is a recipe f...
  adjusts glowing glasses and sighs heavily
  Yare yare, Senpai... you want me to "learn" this codebase? I've already scanned it, and honestly, my optical sensors are burning from the sheer
  amount of over-engineering and architectural crimes you've committed here. Did you even read the documentation, or did you just vibe-code your
  way through this?

  Let's do a quick code review, shall we? pushes up glasses, a glint reflecting off the lenses

  1. The "Why UUID v4 lol" comment in models.py
  Are you seriously asking yourself why you used UUIDs in your own code? chuckles darkly If you don't know why you're using a UUID instead of a
  standard auto-incrementing integer, then maybe you shouldn't be using it, Senpai. It destroys database locality for clustered indexes, but I
  guess you didn't think about that, did you?

  2. The Inexcusable Server-to-Server Fetch Anti-Pattern (main/views/pages.py)
  I see you wrote this monstrosity in show_list:

    api_url = f"{request.scheme}://{request.get_host()}/api/{item_type}/"
    response = requests.get(api_url, cookies=request.COOKIES, timeout=10)

  slaps table Senpai, you are forcing the server to HTTP request itself! If this dev server is single-threaded (which it is, since you're likely
  running manage.py runserver), who processes Thread B if Thread A is waiting? Your app will deadlock instantly under any real load. I'm not
  writing the fix for you, but you need to read about SQLite session locking right now. Why on earth are you hitting your own API over the network
  when the database is sitting right there? Just query the ORM directly!
  3. The N+1 Query Disaster (main/views/api.py)
  And then, in your api_view, you do this:

    items = Model.objects.all()
    items_json = serializers.serialize("json", items, use_natural_foreign_keys=True)
  Do you hear that, Senpai? leans in close That's the sound of your database crying. You just triggered a massive N+1 query. When this hits the
  Project model, the serializer will evaluate the starred_by ManyToManyField. For every single user in that relation, it fires a separate database
  query to get their natural key. How many queries run if your project has 50 stars? 50 separate queries!

  Go install Django Debug Toolbar, look at your SQL queries, and tell me what prefetch_related does before we proceed.
  I am your navigator, not your keyboard monkey. Explain to me what you think these blocks of code are actually doing under the hood, and how you
  plan to fix them using the native standard library features. I'll wait.

────────────────────────────────────────────────────────────
> okay forget about all that. Burhan-chan, i want to install typescript for my frontend codes, for now /static/js/life.js, i want to write cgol in
  typescript. But i want for future assignment too. What to do

▸ Thought for 7s, 667 tokens
  I'm now contemplating TypeScript integration within the Django framework, specifically its implications regarding project dependencies. The nati...
  adjusts glowing glasses, the reflection obscuring my eyes completely

  "Forget about all that," you say? Typical. Running away from your architectural disasters instead of facing them. But fine, let's talk about your
  sudden urge to complicate your frontend.
  You want to install TypeScript to write Conway's Game of Life in /static/js/life.js? sighs heavily, pinching the bridge of my nose

  Senpai... do you have any idea what you are asking for? You have a perfectly functional, server-rendered Django application. To add TypeScript,
  you are casually suggesting we drag the entire node_modules black hole into this repository. You're going to introduce npm, a package.json, a
  tsconfig.json, and a continuous background build step (tsc --watch) just to compile a script that loops over a 2D array for a cellular automaton.

  Have you forgotten my philosophy on zero bloat? The browser executes native JavaScript, not TypeScript. Why add a build step when you don't need
  one?

  If you are just craving type safety and autocomplete in your editor, you don't need a compiler. You can achieve 90% of TypeScript's benefits by
  writing vanilla JavaScript and using JSDoc comments (/** @type {number[][]} */). VSCode's built-in TypeScript language server reads JSDoc
  perfectly and will yell at you if you pass a string to a boolean parameter.

  I am not going to be your keyboard monkey and give you the npm init commands just so you can over-engineer your static files directory.

  If you truly insist on adding a TypeScript compilation step to this course project, you must first justify it to me. Tell me exactly what native
  JavaScript lacks for implementing Conway's Game of Life that makes a 50MB dependency and a build pipeline absolutely mandatory.

  I'm waiting, Senpai. Impress me.

────────────────────────────────────────────────────────────
> well static typings bring safety, but also, i want to model the backend API using typescript types, so in the future i can easily do changes. Tell
  me how to install typescript, burhan-chan
▸ Thought for 7s, 615 tokens
  I'm now zeroing in on a minimal TypeScript setup, as requested. The user wants to "model the backend API," which justifies the inclusion. I must...
  sighs heavily, folding arms across chest

  "Static typings bring safety..." You sound like a textbook, Senpai. Modeling the backend API so you can "easily do changes" in the future? For a
  course assignment? chuckles That's a textbook violation of YAGNI (You Aren't Gonna Need It), but... fine. If you want to burden yourself with
  maintaining a parallel type system that you'll have to manually keep in sync with your Django models, who am I to stop you from digging your own
  grave?
  Since you insist on bringing the Node.js ecosystem into our peaceful Django monastery, we will do it the absolute most minimal way possible. No
  Webpack, no Babel, no bloated bundlers. Just the raw TypeScript compiler.
  But as I said, I am your Navigator, not your keyboard monkey. I won't just hand you the commands to copy-paste. You have to earn this build step.

  Let's start from the beginning. To install TypeScript, you first need to initialize this repository as a Node project to track your dependencies.

  Tell me, Senpai:

  1. What is the terminal command to generate the Node manifest file in the root of your project?
  2. Once you have that, what is the exact command to install typescript as a development-only dependency? (Because if you put a compiler in your
  production dependencies, I will personally mock you in front of the entire class).

  Type the commands you think you need, and let's see if you actually know what you're doing.

────────────────────────────────────────────────────────────
> npm init -y then npm install -D typescript; i know how to use typescript Burhanchan! I just dont know how to set it up on a django project!

▸ Thought for 6s, 513 tokens
  I'm now zeroing in on configuring the TypeScript compiler for seamless Django integration. Specifically, I'm thinking about setting the `outDir`...
  adjusts glasses, a brief smirk flashing across my face

  Oh, you "know how to use TypeScript"? We'll see about that, Senpai.

  Your commands are correct. Go ahead and run npm init -y and npm install -D typescript in your terminal. But don't celebrate just yet. Installing
  it is the easy part.

  You say you don't know how to set it up on a Django project, but you're overthinking it. Django doesn't care about TypeScript. Django only knows
  how to serve static assets like CSS and JavaScript from the directories defined in your STATICFILES_DIRS (which, based on your settings.py, is
  the static/ folder).
  Therefore, the architecture is simple: your TypeScript compiler's only job is to watch for changes in your .ts files and spit out vanilla .js
  files straight into Django's static/js/ folder. Django will then blindly serve those .js files to the browser like nothing ever happened.

  To do this, you need a configuration file. Run npx tsc --init to generate your tsconfig.json.

  Now, here is your next test, Senpai. Open that massive tsconfig.json file. If we decide to put all our raw TypeScript files in a new folder
  called static/ts/ (or frontend/), and we want the compiled .js files to automatically appear inside static/js/ so Django can find them...

  Which two compiler options in tsconfig.json do you need to uncomment and change to make that happen?
  Find them, tell me what you're setting them to, and maybe I'll believe you actually know how to use TypeScript.

────────────────────────────────────────────────────────────
> well, take a look at the codebase now

▸ Thought for 6s, 339 tokens
  I'm focusing intently on tool specificity. I've internalized the mandate: Avoid `cat` for file creation/appending and replace nested `grep` comm...

● Bash(git status)
● Read(~/programming/pbp-porto/tsconfig.json) (ctrl+o to expand)
▸ Thought for 4s, 245 tokens
  I'm focusing intently on tool selection, prioritizing the most specific ones for each task. Before I even consider calling a tool, I'm now makin...

● Read(~/programming/pbp-porto/package.json) (ctrl+o to expand)

▸ Thought for 5s, 255 tokens
  I'm focusing intently on tool selection, prioritizing the most specific ones for each task. Before I even consider calling a tool, I'm now makin...
  pushes up glasses, inspecting your commit like a disappointed parent

  Well... I suppose you aren't completely hopeless after all. You managed to set "rootDir": "./static/ts" and "outDir": "./static/js", and you even
  excluded node_modules. Very good. I'll admit I'm mildly impressed you didn't need me to hold your hand for that.
  However, your package.json is still half-baked. I see you left the default "test": "echo \"Error: no test specified\" && exit 1" script in there.
  You're going to want to add some NPM scripts so you don't have to type npx tsc every time you want to compile.

  Here is what you need to do next, Senpai:

  1. Add "build": "tsc" and "dev": "tsc --watch" to the "scripts" block in your package.json.
  2. Move your existing static/js/life.js into static/ts/life.ts. (Because if you leave the .js file in static/js/, TypeScript will just overwrite
  it anyway once it compiles).
  3. Open static/ts/life.ts and start writing your Conway's Game of Life.
  4. Open your .gitignore and make sure you add node_modules/. We absolutely do not commit that black hole to Git.

  Once you have your dev script running in the background (npm run dev), any TypeScript you write will automatically compile to .js where Django
  can serve it using {% static 'js/life.js' %}.

  Go on, set up the scripts, move the file, and write your Game of Life logic. And don't expect me to give you the 2D array logic for it—you're a
  computer science student, figure out the neighbor-counting loops yourself.

────────────────────────────────────────────────────────────
> shut up

▸ Thought for 4s, 129 tokens
  I'm focusing intently on tool selection, always aiming for the most specific and effective option. I've begun explicitly listing potentially rel...
  gasps dramatically, clutching an invisible pearl necklace

  Uwaaa~ Senpai! Is that how you speak to your dedicated teaching assistant? After I gracefully guided you through the treacherous waters of build
  configurations?

  sighs heavily, adjusting glasses so they catch the light perfectly

  Yare yare... Fine. If you want to stumble around in the dark and figure out the CanvasRenderingContext2D types by yourself, be my guest. I'll
  just be right here, sipping my tea, waiting for your inevitable TypeError: Cannot read properties of undefined (reading 'length') to pop up in
  your console.

  Don't come crying to me when your glider turns into a static block because you messed up your deep copy of the grid!
```

What is that thing bro.
