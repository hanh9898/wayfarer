---
name: initiation-record
description: Write the initiation record — the initiation commitment typed by the learner's own hand, part of the rite of taking a master. Runs only when the learner types /wayfarer:initiation-record themselves; no other skill or role may call it on their behalf, and no content is drafted in advance for them to approve.
disable-model-invocation: true
---

# Initiation Record

## Done when

At least one entry has been written to `~/.wayfarer/initiation-record.md`, word for word as the learner typed it in this very conversation turn — nothing added, nothing removed, no "rewriting it better", not even a spelling fix. The learner may call this skill again to add new entries in later sessions; each call is a new entry, never an edit to an old one.

## When this skill does not help

- The learner wants the AI to write it for them, to suggest a phrasing, or to "smooth out the sentence" before writing it down — refuse outright: a commitment only has value when it is the learner's own words; a sentence drafted by someone else (the AI included) and merely approved is no longer that learner's commitment. Wait for the learner to type it again in their own words; do not offer replacement content.
- The learner has typed nothing yet and only asks "what is an initiation record" — answer briefly what it means (an initiation commitment written by one's own hand), then wait for the learner to type it; do not offer sample content.
- The learner wants to edit or delete an entry written earlier — this skill only adds new entries (append only); it does not edit or delete old ones. State this limit plainly if asked.
- The learner asks about other parts of taking a master (sect name, roles/meridians, the names of the 4 roles) — out of scope for this skill; point them to `/wayfarer:initiation`.

## Present, confirm, write, verify

**Before reading or writing `~/.wayfarer/initiation-record.md`, determine the actual home directory of the machine you are running on** (for example `$env:USERPROFILE` on Windows, `$HOME` on POSIX) instead of assuming a fixed path.

1. **Present:** ask the learner to type their initiation commitment verbatim in their next reply — say plainly that this must be their own words, not a sentence the AI suggested. Once received, repeat it back exactly as written (not one character changed, spelling errors included) so the learner can check it.
2. **Confirm:** ask exactly one short question (for example "write it down exactly as above?") and wait for the learner to agree. If the learner wants a change, go back to step 1 with the version they retyped themselves — not a version the AI fixed for them.
3. **Write:** append a new entry to the end of `~/.wayfarer/initiation-record.md` (creating the file if it does not exist), in this shape:

   ```
   ## <time of writing, ISO 8601 with timezone offset — e.g. 2026-08-27T12:31:57+07:00, or ...Z for UTC>

   <the learner's words, verbatim>
   ```

   Append only — never overwrite or delete existing entries.
4. **Verify:** read back the entry you just wrote from the file and print it for the learner, so they see exactly what was stored. If it differs from the text confirmed in step 2 by even one character, the job is not done — fix it and write it again; do not leave the discrepancy standing.

Once written, if the learner has not finished the other parts of taking a master (sect name, roles/meridians, the names of the 4 roles), give one short reminder to return to `/wayfarer:initiation` and continue — a reminder, not a requirement.

**No other role or skill may write to `~/.wayfarer/initiation-record.md`** — `initiation` included, even though it is what sends the learner here. `initiation` may only read this file to find out whether any entry exists yet (to check the trigger conditions for taking a master); it never writes.

## Load `customize.toml`

This skill exposes no field in `customize.toml` — no customization at this version's scope.

## Why it must be typed by hand, and which layer the lock sits at

A commitment you write yourself before starting a piece of work makes it easier to stay with that work — the effect comes from the act of setting it down yourself, not from the wording. A sentence drafted by someone else and merely approved, however well phrased, does not produce the same effect, because the person approving is not the person who committed.

For that reason, `disable-model-invocation` is set on this skill specifically (and not on `initiation`): the attribute applies to a whole skill, so it has to be split out from `initiation` — merged into one file, the communication-language check in Step 0 of `initiation` would be locked along with it, while that part still needs to self-activate normally when the learner types `/wayfarer:initiation`. Splitting the skill is the only way to lock exactly one behavior (writing the initiation record oneself) without locking a different one by accident.

`disable-model-invocation` locks exactly one thing, at the right mechanical layer: this skill cannot load itself by `description` match — it runs only when the learner types `/wayfarer:initiation-record` verbatim. This is a real Claude Code mechanism, not a convention, so `initiation` — or any other role or skill — cannot *activate* this skill on the learner's behalf.

The rest — not drafting content for the learner to approve, not writing straight into `~/.wayfarer/initiation-record.md` by some other route — has no platform mechanism blocking it; that is convention, held up by the instructions in this file and the write prohibition in `initiation/SKILL.md`. An AI role that misreads or deliberately ignores those instructions — writing the file directly with another tool, or proposing commitment wording inside an `initiation` reply and never calling this skill at all — still gets through, because nothing at the platform layer stops it. Two different layers: the *invocation* lock is a verified mechanism; the *content* lock is a convention, only as strong as whether other skills read and follow the instructions.
