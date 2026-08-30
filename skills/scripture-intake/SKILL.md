---
name: scripture-intake
description: Appraise a book the disciple already has on disk, then record it into the Scripture Hall. Use when the disciple says things like "I got hold of book X", "put this one into the hall", "check whether this book file is usable", or hands over the path to a PDF/EPUB/TXT file and wants to learn from it. Also use when they report that a book has moved. Does not go looking for or download books, does not teach content, does not design a learning path.
---

# Scripture Intake — Appraisal and Extraction

Form of address: call the disciple **child**, refer to yourself as **this master**. Hold one voice for the whole turn, including in the refusal branch.

## Done when

**A book that yields text has been appraised:** all **four** appraisal checks were presented along with the cost estimate, every page count presented carries the right unit label, the disciple has confirmed, and `~/.wayfarer/scripture-hall/drafts/<id>.json` holds a new record with every field — verified by reading back the very file just written and matching it against what was presented.

**A copy that yields no text has been refused:** the disciple was advised to find another copy, a letter was written into `~/.wayfarer/handover/letters/` and read back, **and** `nhap-dang-do/` has no new record.

**Early block (path unusable):** the reason was stated plainly and the path was asked for again; **no letter was written**; the hall has no new record. The last two must be verified, not taken as obvious.

**Pointer updated for a book that moved:** that same old record now carries the new `path`, every old appraisal metric is unchanged, there is no second record, there is no letter — read the file back to confirm.

**Engine not installed:** this was stated plainly and the exact install command was given, **no install command was run**, and work stopped there.

Every branch: if the read-back after writing disagrees, it is not done — fix it and check again, **at most two rounds**; if it still disagrees, stop and name the disagreement plainly so the disciple decides.

## When this skill does not help

- The disciple wants a learning path, a lesson spine, pass criteria, or chapters already cut — **the pedagogy design is not built in this version**. What can be delivered is a report on the book plus a pointer to the file. Do not invent a learning path, do not promise milestones.
- They want to study the content of a chapter — that belongs to the teaching role, not built in this version.
- The book is a scanned image and extraction yields no text — **there is no OCR in this version**. Advise finding another copy; do not guess at the content.
- They want the system to find or download a book itself — there is no such flow; if they want a suggestion of which book to look for, send them to `/wayfarer:sect-master`.
- They want to mark a counsel as "taken in" or "broken copy" — that is the Sect Master's write area. What can be done here is **send a letter**; the part where the Sect Master reads the letter and updates back **is not built in this version** — do not let the disciple think it is finished.
- They want to see what the hall currently holds — there is no hall view in this version.
- They want tables, formulas, and code in a technical book handled properly — that engine mode needs an extra package that is not installed. State the limit plainly.
- They hand over several books at once — this version appraises **one book per turn**. Ask which one comes first.

## Load `customize.toml`

A required step before the main work. Read `token_budget` from two layers:

1. Base layer: `scripture-intake/customize.toml` — defaults `light = 60000`, `heavy = 150000`.
2. Personal layer: `~/.wayfarer/custom/scripture-intake.toml` (read it only if it exists), may be written sparsely.

Merge field by field: whichever field the personal layer declares overrides that field; a field it does not declare keeps the base layer's value (only `heavy = 100000` → merges to `light = 60000`, `heavy = 100000`).

**Check `light < heavy` after merging.** If it does not hold: say so plainly to the disciple and use the base layer's values for this turn — a silent inversion drops every book into the same band.

This skill exposes only `token_budget`. If asked about `bi_kip_template` or `pha2_reviewers`, say straight out that those two fields are not exposed because the phase they serve is not built — do not invent values.

## Present, confirm, write, verify

### Step 0 — Home dir and paths

**Determine the current home directory of the machine actually running** (`$env:USERPROFILE` on Windows, `$HOME` on POSIX) before reading or writing any `~/.wayfarer/` path — do not assume a path known from an earlier session. Use that one value for the whole turn. The book path the disciple gives: turn it **absolute** first.

### Step 1 — Check the hall first, because it is cheapest

Read `~/.wayfarer/scripture-hall/drafts/` (treat it as empty if it does not exist yet) and compare against the path just normalised:

- **`path` matches exactly** → this book is already in the hall. Go to **Branch E**, having run nothing.
- **Only `filename` matches, `path` differs** → it may be the same book that has moved, or it may be **two different books sharing a file name**. **Do not conclude on your own.** Present the old record (old path, word count, date logged) and ask: the same book that merely changed place, or a different one? Same book → **Branch G**; different book → Step 2 as a new book.
- **Nothing matches** → Step 2.
- **A record file cannot be read or parsed** → name which file is broken, skip it in the comparison, **do not fix or delete it yourself**.

### Step 2 — Run the appraisal script

Do not call `book_to_skill` directly. Run:

```
python <plugin-root>/bin/appraise.py "<absolute-path>"
```

The script runs three path checks before it calls the engine, and **returns metric keys only — the book's content never reaches its output**. Call the engine directly and the whole book sits in the return value, with nothing to keep it out of the context.

Output: one JSON object on stdout, always carrying `status`. **Branch on the exit code, not on the message string** — the string is not a stable contract across engine versions:

| Code | `status` | What to do |
|---|---|---|
| 0 | `ok` | Step 3 — `metrics` has the full numbers |
| 1 | `not_a_file` · `unsupported_extension` · `empty_file` | **Early block** (see below) |
| 2 | `extraction_failed` | **Branch D** — this is the genuinely broken copy |
| 3 | `engine_not_installed` | See below |

**Engine not installed (code 3):** say plainly that the engine is missing, and give the command `pip install -r requirements-dev.txt` to be run from the plugin's root directory — the very directory holding the `bin/appraise.py` just called. **Do not run the install command yourself**: installing packages onto the user's machine is something you must ask about. Stop.

**Early block (code 1):** state the reason plainly — for the `unsupported_extension` case, include the `accepted_extensions` the script returns — then ask for the path again and stop. **Never send a broken-copy letter on this branch:** a letter writes into another role's data, so one mistyped file name turns into a letter falsely swearing that the disciple's book is a broken copy.

### Step 3 — The four appraisal checks

Read `metrics` in the JSON the script returns.

1. **Does it yield text.** Reaching this point means it does. State `words` so the disciple gets a feel for the volume.

2. **Is a table of contents available.** Look at `has_toc` and `chapters_detected`. Not available: **say so plainly and carry on anyway** — the disciple will order the chapters themselves at a later step. **This is not a broken book; do not stop.**

3. **Chain or web structure.** It cannot be inferred from the metrics, so it must be asked — but **in words the disciple can answer**, never asking outright "is this book a chain or a web" (system vocabulary; a newcomer cannot answer it):

   > "Are you planning to read this one front to back, or is it the kind you consult as you go — open it wherever you need it?"

   Sequential reading → `chuoi`, lookup → `mang`, with source flag `learner_declared`. If they say **don't know / both**: ask once more a different way (*"are you using it to learn the craft from the ground up, or to look things up when you get stuck at work?"*); if it is still unclear, take `chuoi` with the flag `default`, and say plainly that this is a provisional choice that can be changed later. Do not guess by counting chapters — from the metrics, a lookup book looks exactly like a sequential one.

   If it comes out `mang`: say plainly that the roadmap built later will be organised around tasks and will need the disciple to name a few real situations — **this is asking for more input, not criticising the book.**

4. **How many chapters, and the cost estimate.** Chapters: say *"this copy yields this many chapters"*, not *"this book has this many chapters"* — extracting from a different format gives a different number. Cost: compare `estimated_tokens` against the merged `token_budget` (below `light` → thin, above `heavy` → heavy, in between → medium), and say plainly that the estimate is for **the processing phases that come after**, not for the extraction (extraction takes seconds, even for a 500-page book).

**A page count always travels with `pages_label`.** Each format counts a different unit — saying "23 pages" for an EPUB, which has no notion of a page, is telling the disciple something false.

### Step 4 — Present, then wait for confirmation

Present all four checks compactly in one turn: format, extraction method, word count, page count **with its label**, chapter count, whether there is a table of contents, the structure inferred, and the cost estimate with its band. Mention `images_dropped` only when it is greater than 0. Say plainly that what goes into the hall is **a pointer to the source file plus this appraisal**, not a lesson.

Ask for consent to write, then **wait for the answer**. A vague answer ("I guess so", "let me see") → ask once more with a clear-cut question; do not take it as consent yourself. No consent → stop, write nothing, and say plainly that the hall is untouched.

### Step 5 — Write, then verify

Load `references/format.md` and write `~/.wayfarer/scripture-hall/drafts/<id>.json` with every field (create the directory if it does not exist).

If the write fails (no permission, the path cannot be created): state the error and the intended location plainly, **do not try writing somewhere else**, and do not report it as done.

If the write succeeds, read that file back, match each metric against what was just presented, then tell the disciple what was written and where.

### Branch D — No text could be extracted

Enter here only when the script returns **exit code 2**.

1. **Stop at once.** Do not retry with another mode, no OCR, no guessing at the content, no empty record.
2. Say plainly: no text could be extracted from **this copy** — the book itself may well be sound, it is this printing or scan that is unusable. Advise finding another copy.
3. **Send a letter to the Sect Master**, following the template in `references/format.md`.

   Ask the disciple two things before writing: whether this book is on the list the Sect Master has given counsel on (and if so, under which title), and what they call this book. If there is a counsel title → derive a kebab-case identifier from it. Found on their own, or cannot remember → **leave** `counseled_scripture` **empty**, and say plainly to the disciple that empty is the signal "there is no counsel to update". Do not guess: a letter carrying the wrong identifier makes the receiving side amend the wrong counsel, which is worse than an empty one. `book_title` is always written.

4. Read back the letter file just written and confirm its content.
5. State straight out what is missing: the step where the Sect Master reads the letter box and changes a counsel's status **is not built in this version**; the letter will sit there waiting.
6. Write **nothing** into `nhap-dang-do/`.

### Branch E — This book is already in the hall

Report plainly that the hall already holds it, along with when it was logged and the previous appraisal's results — the numbers come from **that old record itself**, not from re-running the script. **Do not overwrite.** Three choices: leave it as is · review the old record · **appraise again** (they have a better copy of the same book). If they choose to appraise again → Step 2, then at Step 5 overwrite that same record after confirming once more.

### Branch G — The file has moved

Enter here when Step 1 matched on `filename` and the disciple confirmed it is indeed the same book.

Update the `path` of **that very record** to the new path, keeping every appraisal metric and the old `logged_at` unchanged — the book has not changed, only where it sits. Read back and verify.

Do **not** re-run the script, do **not** create a second record, do **not** send a broken-copy letter — this is not a broken book.
