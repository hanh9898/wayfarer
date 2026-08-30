# File formats — `scripture-intake`

Load this file when you reach the writing step (Step 5 or Branch D); there is no need to read it earlier.

## `~/.wayfarer/scripture-hall/drafts/<id>.json`

This role's own write area. One file per book.

```json
{
  "schema": 1,
  "id": "art-of-war",
  "path": "C:/Users/an/Sach/art-of-war.epub",
  "filename": "art-of-war.epub",
  "phase": "appraised",
  "appraisal": {
    "format": "epub",
    "extraction_method": "ebooklib",
    "words": 58389,
    "chars": 335990,
    "estimated_tokens": 77852,
    "cost_band": "medium",
    "pages": 23,
    "pages_label": "spine_items",
    "chapters_detected": 13,
    "chapters_method": "numeric",
    "has_toc": true,
    "images_dropped": 1,
    "structure": "chain",
    "structure_source": "learner_declared"
  },
  "logged_at": "2026-08-28T18:55:37+07:00"
}
```

| Field | What goes in it |
|---|---|
| `id` | kebab-case derived from the book title (drop diacritics, spaces become hyphens, lower case). If the `id` already exists, add a `-2`, `-3`… suffix |
| `path` | the **absolute** path to the original file — a pointer, not a copy |
| `phase` | always `appraised` in this version. Later phases read this field to know the record stopped at appraisal and has no pedagogy layer yet |
| `appraisal` | copied verbatim from the `metrics` the script returns, plus three fields the skill infers: `cost_band`, `structure`, `structure_source` |
| `cost_band` | `light` · `medium` · `heavy` — inferred from `estimated_tokens` against the merged `token_budget` |
| `structure` | `chain` · `web` |
| `structure_source` | `learner_declared` when the learner answers clearly · `default` when they say they do not know. No other value exists in this version |
| `logged_at` | ISO 8601 with a timezone offset, or `Z` for UTC |

**Never write a `text` key into this file** — the script does not return it, so it has no road here; do not add it by some other route.

## `~/.wayfarer/handover/letters/<id>.json`

The shared mailbox — every role sends, every role reads. One file per letter.

```json
{
  "schema": 1,
  "from": "scripture-hall",
  "to": "sect-master",
  "kind": "report_damaged_copy",
  "counseled_scripture": "art-of-war",
  "book_title": "The Art of War",
  "reason": "EPUB renamed to .pdf; the engine could not extract text after the path, extension and size checks all passed",
  "status": "waiting"
}
```

| Field | What goes in it |
|---|---|
| file `id` | kebab-case from `book_title`, **with a timestamp suffix** (`<title>-<YYYYMMDDHHmm>.json`). Without the suffix, sending the same book a second time overwrites the earlier letter — and the mailbox is append-only |
| `counseled_scripture` | the kebab-case identifier of the counsel this book came from. **An empty string when the book came from no counsel** — do not guess |
| `book_title` | the book's title exactly as the learner says it, **always written**. This is the fallback matching route when a regenerated identifier finds no line on the Sect Master's side |
| `reason` | the observable truth: which format, which step it broke at. Do not paste the engine's raw error string |
| `status` | `waiting` when just sent. This role never changes that value — handling the letter belongs to the receiver |

This role **does not** read and **does not** write `sect-master/counsel.jsonl` or `counsel-broken.jsonl` in any form whatsoever.
