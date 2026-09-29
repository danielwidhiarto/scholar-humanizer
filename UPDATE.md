# Scholar Humanizer v1.2.0 — Rencana Pembaruan

Dokumen ini menetapkan scope v1.2.0 setelah cross-check terhadap tiga referensi. Tujuannya mengambil teknik yang berguna tanpa menyalin aturan umum yang bertentangan dengan konvensi akademik.

> **Status:** Scope v1.2.0 (Job 1–5 dan dua permintaan format lanjutan) telah diimplementasikan dan divalidasi.
> **Batas scope:** v1.2.0 berfokus pada aturan inti, perlindungan integritas naskah, contoh regresi, dan sinkronisasi dokumentasi. Installer multi-agent dan linter khusus ditunda.
> **Prinsip utama:** Aturan section-aware Scholar Humanizer tetap menjadi sumber perilaku; pola dari referensi menjadi heuristik kontekstual, bukan larangan universal.

**Sumber yang diperiksa:**
- [humanizer `SKILL.md`](https://github.com/blader/humanizer/blob/main/SKILL.md) dan [README](https://github.com/blader/humanizer)
- [stop-slop `SKILL.md`](https://github.com/hardikpandya/stop-slop/blob/main/SKILL.md), [phrases](https://github.com/hardikpandya/stop-slop/blob/main/references/phrases.md), dan [structures](https://github.com/hardikpandya/stop-slop/blob/main/references/structures.md)
- [anti-slop core](https://github.com/miqdadbadjuber/anti-slop/blob/main/antislop.md) dan [copywriting skill](https://github.com/miqdadbadjuber/anti-slop/blob/main/skills/antislop-copywriting/SKILL.md)

---

## 1. Hasil Cross-check dan Batas Adopsi

### A. `humanizer`

- Versi `SKILL.md` pada `main` saat diperiksa mencantumkan 26 pola yang bersumber dari panduan Wikipedia *Signs of AI writing* dan tinjauan teks AI.
- Lima pola pertama diprioritaskan sebagai tell terkuat. Satu kemunculan cukup untuk diperiksa, tetapi bukan berarti selalu harus dihapus: kontras, kalimat pendek, atau penutup boleh dipertahankan jika membawa informasi baru atau memang sesuai suara penulis.
- Voice sample dapat mengesampingkan aturan gaya umum, termasuk penggunaan dash. Mode teks tempel menampilkan draft, kritik singkat, dan versi akhir; mode file menulis versi akhir saja dan mengubah prosa, bukan kode, metadata, data, atau target tautan.
- Prinsip no-fabrication dan pencocokan voice sample sudah ada di Scholar Humanizer saat ini. Jangan mencatatnya sebagai fitur baru dari v1.2.0.
- Tujuan humanisasi adalah memperbaiki suara dan keterbacaan, bukan mengakali AI detector. Humanizer sendiri secara eksplisit menyatakan detector bukan targetnya.

### B. `stop-slop`

- `SKILL.md` saat ini memiliki **8 Core Rules**, bukan 7. Rubriknya memakai lima dimensi berskala 1–10 dengan revisi di bawah 35/50.
- Yang relevan untuk diadaptasi: pemangkasan filler, pengenalan struktur formulaik, variasi ritme, dan penilaian kualitas sebagai masukan.
- Aturan seperti wajib active voice, membuang semua adverb/hedging, atau selalu menyapa pembaca dengan “you” adalah aturan umum stop-slop dan **tidak** boleh diterapkan mentah pada naskah akademik.

### C. `anti-slop`

- Core anti-slop terutama ditujukan untuk UI dan pekerjaan coding. Skill copywriting-nya lebih relevan untuk prosa: jangan mengarang fakta, jangan mensterilkan voice, dan tandai actorless passive hanya saat mengaburkan pelaku.
- Tiga tier sumber adalah **Hard Gate**, **Purpose-Gate**, dan **Quality Locks**. Empat blok Delivery Gate-nya adalah **Hard Gate**, **Purpose-Gate**, **Liveliness**, dan **Craftsmanship & Quality Locks**. Nama blok Integrity/Vocabulary/Rhythm/Conformance dalam dokumen ini adalah rancangan Scholar Humanizer, bukan istilah dari anti-slop.
- Mode sumber adalah **DURING** (terapkan saat membuat) dan **AFTER** (audit hasil yang sudah ada). Mode **Audit** dan **Surgical Rewrite** di bawah adalah adaptasi untuk Scholar Humanizer, bukan nama mode asli.
- “Filter vs Direction” pada sumber membedakan filter dari arahan desain seperti `DESIGN.md`. Untuk Scholar Humanizer, konsep ini diterjemahkan menjadi filter pola AI plus arahan yang benar-benar diberikan pengguna: sampel tulisan, bidang, section, dan pedoman jurnal.
- Installer anti-slop menggunakan jalur Node/`npx`; `scripts/install.py` zero-dependency dalam rencana awal adalah fitur baru, bukan sesuatu yang disediakan referensi.

---

## 2. Matriks Harmonisasi untuk Naskah Akademik

Prinsipnya: pertahankan aturan section-aware yang sudah ada. Pola dari referensi adalah sinyal untuk ditinjau, bukan pemicu rewrite otomatis.

| Pola / aturan sumber | Keputusan untuk Scholar Humanizer | Aturan operasional |
|---|---|---|
| **Lima tell terkuat Humanizer** | **Prioritas tinggi, bukan hard ban** | Periksa fungsi kalimat dan konteks. Hapus jika hanya memberi drama atau mengulang klaim; pertahankan jika menambah fakta, mengoreksi asumsi nyata, atau memang sesuai voice penulis. |
| **Binary contrast / “not X but Y”** | **Kontekstual** | Hapus kontras kosong atau lawan-argumen fiktif. Pertahankan kontras yang membedakan metode, hipotesis, hasil, atau interpretasi secara substantif. |
| **Forced triads, dramatic fragments, one-line closers** | **Kontekstual** | Tandai pola yang berulang atau dibuat demi efek. Jangan menghapus daftar tiga item yang memang mencerminkan kategori/data, kalimat singkat yang membawa hasil baru, atau penutup dengan implikasi spesifik. |
| **Active voice / passive voice** | **Gunakan matriks section lokal** | Methods: passive voice dipertahankan sesuai panduan repo. Abstract, Discussion, dan Conclusion: passive voice dihindari; Introduction, Literature Review, dan Results: diperbolehkan. Ikuti matriks SKILL.md dan instruksi target; jangan menerapkan aturan active voice universal dari stop-slop. |
| **Inanimate subjects / false agency** | **Batasi ke personifikasi yang mengaburkan pelaku** | “The data suggest” dan “Results indicate” adalah bentuk akademik yang wajar. Tandai ungkapan seperti “the data tells us” jika memberi data agensi manusia atau menutupi pelaku yang penting. |
| **Hedging, adverbs, dan transitions** | **Section-aware** | Pertahankan hedging yang mencerminkan ketidakpastian ilmiah, terutama di Discussion. Pangkas hedge bertumpuk atau filler; jangan membuang semua adverb atau transisi secara mekanis. |
| **Em dash / en dash** | **Ikuti kebijakan gaya dan format** | Pertahankan gaya dari sampel penulis bila relevan. Jangan mengubah dash yang bermakna dalam rentang angka, simbol, atau sintaks LaTeX. |
| **“You” vs “people” / first person** | **Jangan dijadikan hard gate** | Hindari sapaan langsung jika register atau pedoman jurnal mengharuskannya. Penggunaan “we” mengikuti section, sampel penulis, dan instruksi target jurnal. |
| **Filter vs Direction** | **Adaptasi lokal** | Filter mengurangi pola AI; Direction hanya berasal dari sampel penulis atau pedoman yang diberikan/diminta. Jangan mengasumsikan Nature, IEEE, atau bidang tertentu punya satu gaya universal. |
| **Rubrik 35/50 dan Delivery Gate** | **Rubrik sebagai panduan, bukan bukti objektif** | Pertahankan rubrik Scholar Humanizer yang sudah ada. Dalam gate lokal, Integrity boleh PASS/FAIL; deteksi pola, ritme, dan voice dilaporkan sebagai temuan yang perlu penilaian. |

**Batas klaim:** jangan menyatakan suatu pola “100% slop” hanya dari frasa tunggal. Jangan menyatakan sitasi sudah terverifikasi jika sumber pembanding tidak tersedia.

---

## 3. Alur Perilaku yang Diusulkan

Mode **Audit** dan **Rewrite** adalah pilihan produk Scholar Humanizer. Pengguna tidak perlu ditanya berulang kali jika maksudnya sudah jelas.

```text
[ INPUT: teks atau file .tex / .md / .docx / .txt ]
                         |
                         v
[ PILIH / INFER: Audit (tanpa edit) atau Rewrite (edit minimal) ]
                         |
                         v
[ ARAHAN: section + sampel penulis + pedoman target jika diberikan ]
                         |
                         v
[ PROTEKSI: klaim, angka, satuan, sitasi, math, label/ref, sintaks file ]
                         |
                         v
[ DETEKSI: pola prioritas tinggi + pola lain sesuai konteks/cluster ]
                         |
                         v
[ AUDIT: temuan saja ]                 [ REWRITE: revisi prosa minimal ]
             \                                      /
              +------ [ cek integritas dan section fit ] ------+
                                      |
                                      v
[ OUTPUT: temuan yang dapat ditindaklanjuti atau teks akhir + ringkasan ]
```

### Rincian dan kriteria

1. **Mode**
   - **Audit:** tidak mengubah file; laporkan kutipan/temuan, alasan, dan saran. Sertakan nomor baris hanya jika file sumber dan barisnya tersedia secara langsung.
   - **Rewrite:** ubah prosa sesedikit mungkin sambil mempertahankan makna, klaim, dan voice. Berikan teks akhir dan ringkasan singkat.
   - Jika permintaan tidak membedakan audit dan rewrite dan pilihan itu mengubah hasil secara material, tanyakan sekali. Jangan menjadikan pertanyaan ini langkah wajib untuk setiap penggunaan.
2. **Arahan**
   - Gunakan matriks section Scholar Humanizer yang ada.
   - Sampel penulis dan pedoman jurnal yang diberikan pengguna mengalahkan heuristik umum. Jangan mengarang profil gaya jurnal atau mengasumsikan “Nature aktif” / “IEEE pasif”.
3. **Perlindungan naskah**
   - Untuk `.tex`, jangan mengubah perintah LaTeX, key sitasi, label/ref, rumus, atau struktur markup ketika hanya diminta mengedit prosa.
   - Perlakukan materi yang tidak dapat dipastikan sebagai sintaks sebagai terlindungi dan laporkan, jangan menebak atau menulis ulang.
   - Dukungan LaTeX ini adalah persyaratan perilaku baru; bukan fitur yang diklaim telah ada di ketiga referensi.
4. **Pemeriksaan akhir Scholar Humanizer**
   - **Integrity (hard gate):** tidak ada fakta, angka, satuan, klaim, atau sitasi baru/hilang/berubah tanpa dasar yang diberikan. Jangan menyatakan sitasi terverifikasi jika sumbernya tidak diperiksa.
   - **Pattern review (diagnostik):** laporkan pola dengan konteks; tidak perlu menghasilkan “0 kata terlarang”.
   - **Section/voice conformance:** cek matriks section, sampel penulis, dan pedoman target yang tersedia.
   - **Quality review (advisory):** gunakan rubrik yang ada untuk precision, voice, flow, economy, dan integrity. Skor bukan bukti objektif atau pengganti penilaian akademik.
   - Empat blok di atas adalah rancangan gate lokal. Jangan mengatribusikannya sebagai blok Delivery Gate anti-slop.
5. **Integritas dan tujuan**
   - Jangan mengoptimalkan teks untuk melewati AI detector.
   - Untuk file, ubah prosa saja; pertahankan kode, frontmatter, data, link target, perintah, dan konten teknis sesuai kebutuhan format.

---

## 4. Distribusi dan Kompatibilitas Agent

### Scope v1.2.0

- Pertahankan format skill Markdown yang harness-neutral; jangan membuat klaim dukungan agent yang belum diuji.
- Evaluasi `npx skills add danielwidhiarto/scholar-humanizer` sebagai jalur distribusi standar, lalu verifikasi bahwa CLI mengenali struktur repo sebelum menambahkannya ke README.
- Pertahankan petunjuk instalasi manual sebagai fallback.
- **Tidak termasuk v1.2.0:** `scripts/install.py`, injeksi pointer ke file konfigurasi agent, dan tabel 12-agent dengan path yang belum diverifikasi.

### Jika installer multi-agent diprioritaskan di rilis berikutnya

1. Tetapkan daftar agent yang benar-benar diminta pengguna dan cakupan project/global.
2. Verifikasi tiap path serta mekanisme pointer dari dokumentasi resmi agent pada saat implementasi; pisahkan folder skill, plugin, dan file instruksi.
3. Uji instalasi, update, dan uninstall. Jangan mengandalkan path dari tabel referensi lama.
4. Catat bahwa installer anti-slop sendiri memakai jalur Node/`npx`; installer Python zero-dependency akan menjadi solusi baru yang perlu desain dan pengujian tersendiri.

Catatan dokumentasi (selesai): pembuka README dibuat harness-neutral. `npx skills add danielwidhiarto/scholar-humanizer --list` mengenali satu skill; smoke test instalasi lokal dengan `--copy` juga berhasil di project sementara yang terisolasi. Instalasi manual tetap tersedia sebagai fallback.

---

## 5. Job List v1.2.0

> **Status checklist:** Job 1–5 dan kedua permintaan format lanjutan selesai.
> **Urutan:** Scope awal v1.2.0 sudah diimplementasikan sesuai urutan Job 1–5.

### Scope rilis

- [x] **Job 1 — Memperjelas aturan inti (`SKILL.md`, `rules/academic_voice.md`, `rules/ai_slop.md`, `references/banned_phrases.md`)**
  - Terapkan pola AI sebagai heuristik kontekstual; jangan menjadikan lima tell Humanizer sebagai larangan mutlak.
  - Pertahankan matriks section yang sudah ada. Rapikan klaim passive voice agar Discussion juga konsisten dengan SKILL.md.
  - Tinjau false positive “The data suggest” dan bedakan ungkapan akademik itu dari false agency seperti “the data tells us”.
  - Pertahankan hedging, transisi formal, terminologi, dan passive voice sesuai section; sampel penulis tetap mengalahkan aturan gaya umum.
  - Susun pemeriksaan akhir lokal menjadi integrity hard gate, pattern review diagnostik, section/voice conformance, dan quality review advisory.
  - **Selesai jika:** aturan tidak lagi menyebut semua kontras, passive voice, adverb, hedging, atau dash sebagai slop tanpa konteks; `SKILL.md` tetap maksimal 200 baris.

- [x] **Job 2 — Menambahkan perlindungan format dan contoh regresi**
  - Tegaskan bahwa rewrite `.tex` mengubah prosa saja dan mempertahankan math, perintah, citation keys, labels, refs, angka, dan satuan.
  - Tambahkan contoh untuk: kontras kosong vs. kontras bermakna; penutup dramatis vs. hasil faktual; passive voice Methods; hedging Discussion; “the data suggest” vs. personifikasi; sampel penulis yang memakai dash.
  - Tambahkan aturan kontekstual untuk mengubah arrow-chain menjadi prosa saat berfungsi sebagai outline naratif, serta mempertahankan numbering sambil merapikan bullet terkait bila aman.
  - Tambahkan kasus LaTeX pada contoh/cek manual: math inline dan multiline (`align`, `gather`), `\cite{...}` ganda, `\label`/`\ref`, dan `\%`.
  - **Selesai jika:** contoh menunjukkan pola yang perlu dihapus sekaligus false positive yang harus dipertahankan; arrow, numbering, dan bullet diperlakukan sesuai konteks; tidak ada perubahan terhadap sintaks atau nilai yang dilindungi.

- [x] **Job 3 — Menyelaraskan rubrik dan contoh**
  - Pertahankan rubrik Scholar Humanizer yang sudah ada: Precision, Voice, Flow, Economy, Integrity; ambang 35/50 digunakan sebagai panduan revisi.
  - Perjelas bahwa skor adalah penilaian kualitatif, bukan ukuran objektif humanisasi dan bukan klaim tentang deteksi AI.
  - Perbarui `examples/scoring_examples.md` dan `examples/before_after.md` jika aturan atau contoh berubah.
  - **Selesai jika:** contoh dan README menjelaskan rubrik yang sama dengan SKILL.md dan tidak memberi kesan bahwa skor membuktikan keaslian teks.

- [x] **Job 4 — Sinkronisasi dokumentasi dan versi**
  - Sinkronkan `README.md`, `CHANGELOG.md`, `AGENTS.md`, dan dokumen aturan dengan perilaku yang benar-benar diterapkan.
  - Perbaiki pembuka README agar tidak membatasi skill pada Claude Code; dokumentasikan jalur `skills` hanya setelah uji instalasi berhasil.
  - Perbarui background/credits dengan batas adopsi yang akurat: stop-slop memiliki 8 aturan; humanizer menampilkan 26 pola; audit/rewrite dan gate Scholar adalah adaptasi lokal.
  - Ubah `metadata.version` dari 1.1.0 ke 1.2.0 hanya saat perubahan perilaku rilis sudah diterapkan.
  - **Selesai jika:** SKILL.md, README, rules, references, examples, dan changelog tidak saling bertentangan.

- [x] **Job 5 — Validasi paket**
  - Jalankan validator yang sudah ada: `python3 scripts/validate-package.py`.
  - Periksa frontmatter, keberadaan file paket, dan batas 200 baris SKILL.md.
  - **Jangan** menambah validasi keberadaan `install.py` atau `academic-slop-checker.py` pada rilis ini karena kedua script tersebut ditunda.
  - **Selesai jika:** validator menghasilkan `Scholar Humanizer v1.2.0 is valid` setelah Job 4 membump versi.
  - **Hasil:** di Windows, validator dijalankan dengan `python scripts\validate-package.py` dan menghasilkan `Scholar Humanizer v1.2.0 is valid`.

## 6. Permintaan Format Lanjutan (Selesai)

Kedua preferensi berikut sudah diterapkan pada `SKILL.md`, rules, README, dan contoh regresi.

- [x] **Permintaan 1 — Mengubah rangkaian panah menjadi paragraf saat digunakan sebagai prosa**
  - Jadikan rangkaian istilah yang dipisahkan panah sebagai paragraf/sentence hanya ketika konteksnya narasi akademik.
  - Pertahankan panah pada diagram, rumus, kode, atau workflow yang memang membutuhkan notasi visual.
  - Jaga urutan dan relasi yang dinyatakan sumber; jangan menyimpulkan kausalitas atau urutan tindakan baru.
  - **Selesai jika:** aturan dan contoh regresi menangani prosa vs. diagram secara berbeda tanpa mengubah makna.

- [x] **Permintaan 2 — Mempertahankan numbering dan mengurangi bullet non-numbered pada prosa**
  - Pertahankan numbering untuk temuan atau langkah berurutan.
  - Ubah bullet non-numbered yang saling terkait menjadi paragraf hanya jika keterbacaan dan semua klaim tetap terjaga; pertahankan bullet untuk item independen atau format yang diminta.
  - Contoh regresi memakai isi generik; tidak menyalin paper Grad-CAM.
  - **Selesai jika:** aturan dan contoh regresi menjaga numbered list serta menunjukkan konversi bullet ke paragraf tanpa kehilangan klaim.

### Ditunda dari v1.2.0

- **Installer 12-agent:** pertimbangkan setelah ada kebutuhan pengguna dan matriks dukungan resmi yang teruji. Jangan mencampur path project/global, plugin, skill folder, dan pointer.
- **`scripts/academic-slop-checker.py` dan laporan Overleaf:** perlu spesifikasi dan rilis terpisah. Linter hanya boleh menandai kandidat pola, bukan memutuskan “slop” atau PASS/FAIL dari pencocokan kata.
- **Nomor baris / `Ctrl+G`:** jangan menjanjikan akurasi atau shortcut Overleaf sebelum diverifikasi pada file dan dokumentasi target.
- **Manifest dan integrasi khusus agent:** buat hanya setelah jalur standar skill diuji dan kebutuhan spesifiknya jelas.
