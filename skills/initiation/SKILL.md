---
name: initiation
description: Take a master and enter the sect in Wayfarer. Use when the learner types /wayfarer:initiation — first install of the plugin, wanting to check or reset the communication language, or master-taking not yet finished (naming the sect, declaring role/meridian, naming the 4 companion roles). The first step of every learning journey.
---

# Initiation

## Done when

The communication language (`communication_language`) has been confirmed (Step 0), **and** the master-taking rite is active — meaning the profile holds a sect name, a role, a meridian, and personal names for the 4 roles that speak to the learner, **and** an initiation record the learner typed themselves (`~/.wayfarer/initiation-record.md` has at least one entry). If any of these is missing, say plainly where things stand, do not treat it as done, and do not pretend the master-taking rite is active when it is not.

Counsel (the Sect Master naming a specific book for the learner to go find) is the step that follows immediately after master-taking — once the four parts below are complete, point the learner to `/wayfarer:sect-master` (see Step 6).

## When this skill does not help

- The learner has finished taking a master (profile plus initiation record) and only wants to continue an unfinished scripture — use `/wayfarer:seclusion` instead of calling `initiation` again.
- The learner wants a specific book named right after finishing master-taking (counsel) — not the job of `initiation`; point them to `/wayfarer:sect-master`, and do not invent a book title to fill the gap.
- The learner asks about realm breakthrough or levelling up, or any feature belonging to a later part of the path — not built in this version; answer plainly "not supported in this version", do not guess, do not silently skip — whether they ask in the middle of master-taking or at any other point in the conversation.
- The learner asks this skill (or any role) to write or pre-draft the initiation record for them to approve — not possible in any form, not even as a suggested sample sentence; refuse and point them to `/wayfarer:initiation-record` so the learner types it themselves.

## Present, confirm, write, verify

Step 0 writes no new state (it only reads the existing `userConfig`). From Step 2 onward (naming the sect, declaring role/meridian, naming the 4 roles), every write to `~/.wayfarer/sect-master/profile.json` follows the same order: **present** the content about to be written for the learner to review → **confirm** that they agree → **write** (update only the relevant field, never silently overwrite the whole file — other fields already in the profile stay as they are) → **verify** by reading back the very file just written. If the read-back differs from what was confirmed, return to the present step with the exact mismatch as context; do not treat the write as finished.

Writing the initiation record (`~/.wayfarer/initiation-record.md`) follows the same four steps, but it lives in a separate skill, `initiation-record` — see Step 3 below. `initiation` never writes that file itself.

## Load `customize.toml`

This skill exposes no field in `customize.toml` — no customization within the scope of this version.

## Step 0 — Check the communication language

The `communication_language` value the learner has configured (Claude Code substitutes it here when the
skill loads; it is not the static value declared in `plugin.json`):

```
${user_config.communication_language}
```

**Do not read `.claude-plugin/plugin.json` directly to get this value** — that file declares only the
*schema* (type, title, a suggested `default`), not the value the learner actually set; the real value
lives in `pluginConfigs["wayfarer@wayfarer"].options` in Claude Code's `settings.json`, and the correct
way to read it is through the `${user_config.communication_language}` substitution above — verified by
running it: reading `plugin.json` directly always shows `default: "Vietnamese"` no matter what the
learner configured, so it cannot tell "not set" apart from "set to exactly the default value".

- **The substitution line above shows a concrete language value** (e.g. `Vietnamese`, `English` — as
  opposed to the literal placeholder string `${user_config.communication_language}` reproduced just
  above): that is the configured value — use it for every reply from here on in this session. Do not
  ask the learner again — not even in a later session, because this is durable plugin configuration
  that Claude Code reloads on its own.
- **The substitution line above is empty, or still shows the literal placeholder `${user_config.communication_language}`
  unsubstituted** (both mean no value has been configured — the substitution mechanism may leave the
  line blank or leave the syntax intact when the field is unset, so do not assume one fixed form):
  tell the learner plainly that the communication language is not set, and guide them to run:

  ```
  /plugin configure wayfarer@wayfarer
  ```

  This is a user-level Claude Code command — the skill cannot run it on their behalf. Once the learner has run it and set a value, call `/wayfarer:initiation` again to continue.

**Do not assume Claude Code asks automatically when the plugin is first enabled** — the CLI install path without `--config` only prints a warning; it does not block or prompt (verified). This Step 0 is the only place that actively checks and reminds; do not count on any other mechanism to do it instead.

## Throughout master-taking

From Step 1 onward, whenever the learner asks about realm breakthrough or levelling up in the middle of master-taking, answer immediately and plainly "not supported in this version" — do not guess, do not silently skip — then return to the exact step in progress, and do not let the question derail the whole conversation.

## Step 1 — Check how far the master-taking profile has got

**Before reading or writing any path under `~/.wayfarer/` in this session, determine the actual home directory of the machine you are running on** (for example `$env:USERPROFILE` on Windows, `$HOME` on POSIX) rather than assuming a path — nothing guarantees it is the same as last time. Use that one determined value for every remaining step of this session.

Read `~/.wayfarer/sect-master/profile.json` (if it exists) and `~/.wayfarer/initiation-record.md` (if it exists — read only, never write to this file, see Step 3) to find out which of the four parts below are already done:

| Part | Done when |
|---|---|
| Sect name | `profile.json` has a non-empty `ten_mon_phai` field |
| Initiation record | `initiation-record.md` exists and has at least one entry |
| Role + meridian | `profile.json` has both `vai` and `mach` non-empty |
| Names for the 4 roles | `profile.json` has `role_names` with all four keys: `sect-master`, `scripture-hall-elder`, `tome-spirit`, `examiner` |

- **All four parts present:** the master-taking rite was already activated earlier. Do not repeat any question from the steps below — summarize the existing profile (sect name, role, meridian, names for the 4 roles) for the learner, say plainly that master-taking is finished, then stop here (see Step 6 for how to answer the "what comes next" part).
- **One or more parts missing:** continue with the steps below, but **skip whatever is already done** — do not re-ask for anything already in the profile. Priority order when several are missing: sect name → initiation record → role + meridian → names for the 4 roles.

## Step 2 — Name the sect

Skip this step if `ten_mon_phai` is already in the profile (see Step 1).

Ask the learner what they want to name their own sect — a playful name that gives the profile some identity; it carries no technical meaning. The learner types it freely, with no restriction on form.

- Present: repeat the name received back verbatim so the learner can check it (in case of a typo).
- Confirm: ask once, briefly, and wait for the learner to agree.
- Write: save it to the `ten_mon_phai` field in `~/.wayfarer/sect-master/profile.json` (create the file and directory if absent; if the file already exists, add or change only this field and leave every other field as it is).
- Verify: read back the file just written and confirm the name saved is the one agreed on.

Renaming the sect later (if the learner wants to) changes only this field's value — no new profile, no renamed directory or file; the profile must never be lost along with the name.

## Step 3 — Guide them to write the initiation record

Skip this step if `~/.wayfarer/initiation-record.md` already has at least one entry (see Step 1).

The initiation record is a commitment to initiation typed by the learner's own hand — not a sentence the AI drafts in advance for the learner to skim and approve. Tell the learner why: a commitment can steer a journey only when it is the writer's own words; a sentence drafted by someone else, however good it sounds, does not produce the same effect.

Guide the learner to run exactly this command:

```
/wayfarer:initiation-record
```

This is a separate skill, and **it runs only when the learner types this command themselves** — `initiation` (the current skill) cannot call it on their behalf, and must never pre-draft initiation record content in any form, not even a single sample sentence "to make starting easier". If the learner asks you to "just write one sentence for me", refuse outright, explain exactly the reason above, and still point them back to the command so they type it themselves.

The learner can run this command in the very next exchange, or leave it for a later session — the profile and the master-taking progress are not lost between steps. Once it is done, call `/wayfarer:initiation` again to continue the remaining steps; Step 1 will recognize this part as finished and will not ask again.

Nothing forces the learner to finish this step before moving on to Step 4 or 5 if they want to keep going — just remember to state clearly at Step 6 that the master-taking rite is still NOT active until this step is done.

## Step 4 — Declare role + meridian

Skip this step if both `vai` and `mach` are already in the profile (see Step 1).

Ask the learner: do they already know what they want to train (role + meridian)?

**The "already knows" branch:** let the learner state both the role (the trade or role they currently work in, for example tester, BA, developer) and the meridian (the skill or direction they want to train, for example software testing, business analysis) directly — there is no fixed list to choose from; record exactly what the learner says.

**The "does not know yet" branch** (the learner says "don't know yet" / "not sure" / anything equivalent):

1. Ask for the ROLE first — in the spirit of "what trade do you ply?" — and **do not ask for the meridian first**: the meridian is a concept internal to the system, and a newcomer cannot answer it.
2. From the role just received, suggest a fitting meridian, labelled with the suggestion's actual confidence:
   - Real data exists from several learners in the same role (roughly 5 or more) → suggest it with the concrete numbers.
   - No real data, but a specific reference source to lean on → suggest it and name that source.
   - Neither of the two (the current state — the store is still new) → suggest it with an explicit warning: this is inference, not real data.
   - At every level, always include the way out: "type a different meridian if the suggestion does not fit".
3. Offer the suggestion (carrying the source flag above) for the learner to choose, or let them type a different meridian — **never settle on a meridian without asking the learner**.

- Present: repeat the role + meridian just settled on (and the source: self-declared, or inferred from the role).
- Confirm: ask again and wait for the learner to agree before writing.
- Write: save `vai`, `mach`, and `meridian_source` (`self_declared` if the learner declared it directly or typed their own in the "does not know yet" branch; `inferred_from_role` if the learner accepted the suggestion inferred from the role) into `~/.wayfarer/sect-master/profile.json`.
- Verify: read the file back and confirm the role, meridian and source saved are the ones agreed on.

## Step 5 — Name the 4 roles

Skip this step if `role_names` already has all four keys in the profile (see Step 1).

Name only the four roles that speak to the learner directly: Sect Master, Scripture Hall Elder, Tome Spirit, Examiner. Do not ask for a name for any other role — the rest never appear before the learner, so naming them means nothing to them.

Offer a few names for each role (illustrative examples, not a list they must pick from):

- Sect Master: "Bạch Vân", "Huyền Cơ"
- Scripture Hall Elder: "Mặc Thư", "Tàng Vân"
- Tome Spirit: "Nhã Tri", "Minh Tuệ"
- Examiner: "Thanh Nghiêm", "Chính Trực"

The learner picks one of the suggestions, types a different name, or keeps the original role name — all three are valid, and **do not force a choice from the list**.

- Present: list all four pairs (original role name → the name the learner chose) so the learner can review them in one pass.
- Confirm: ask again, wait for agreement, and allow edits if the learner changes their mind on any role.
- Write: save into `role_names` in `~/.wayfarer/sect-master/profile.json` under exactly these four technical keys: `sect-master`, `scripture-hall-elder`, `tome-spirit`, `examiner`.
- Verify: read the file back and confirm all four keys are present with the names just saved.

## Step 6 — Confirm master-taking

Read the profile and `initiation-record.md` once more (the same check as in Step 1):

- **All four parts present** (sect name, initiation record, role + meridian, names for the 4 roles): say plainly that the master-taking rite is active, and summarize the whole finished profile for the learner using the exact names they gave the 4 roles. Point explicitly to the next step: invite the learner to type `/wayfarer:sect-master` themselves to receive counsel on a specific book — do not switch over automatically, do not call it on their behalf; if the learner immediately asks "so what do I study now", answer with exactly that invitation to run the command, and do not invent a book title here.
- **Only the initiation record is missing, every other part present:** say plainly that **the master-taking rite is NOT active** — do not pretend it is finished just because the role, meridian and names for the 4 roles are all there — mention the `/wayfarer:initiation-record` command exactly once, but do not block the conversation here if the learner does not want to do it right away.
- **Some other part is missing** (sect name, or role/meridian, or names for the 4 roles): it is not time to confirm — return to the corresponding step above first.
