---
name: setup
description: Sets up company-os for a company - asks about the business, writes the company-os folder (facts, rules, team, approvals, log), turns on the approval gate and schedules the morning standup and night report. Use when someone installs company-os, says "set up my company", or wants to change their company details, desks or times.
disable-model-invocation: true
argument-hint: "[folder for company-os, default ./company-os]"
---

# Set up company-os

Goal: in one sitting, turn this generic plugin into the operating team for the user's company. Write nothing until
you've collected the answers. Templates are in `${CLAUDE_PLUGIN_ROOT}/templates/`.

Current setting for the company folder: `${user_config.company_dir}` (empty means first-time setup). If it's set and
the folder exists, this is an update: read the existing files, show what's there, and only ask about what the user
wants to change.

## 1. Read before you ask

Look in the current project for anything that already describes the company: `README.md`, `CLAUDE.md`, `AGENTS.md`,
`BUSINESS.md`, a website repo, pricing pages, brand or style guides. Pre-fill answers from them and show the user what
you found, so they confirm instead of retyping. Note each file you used; it goes under "Deeper sources" in `company.md`.

## 2. Ask (AskUserQuestion, at most 4 questions per call; free text where options don't fit)

Round 1, the company:
- Company name, one line on what it does, website.
- Owner name and the email the standup and night report go to.
- Time zone.
- What you sell (offers and prices) and who buys. If a facts file already holds this, point to it instead.

Round 2, the operation:
- Which desks to turn on now: Sales, Content, Social, Website & SEO, Ops & Finance. Recommend starting with **none or
  one**: week 1 is only the standup and night report. Desks not picked are written as **off**.
- Channels and accounts (social handles, newsletter, blog).
- Tools already connected in Claude (Gmail, Google Drive, a social scheduler, GitHub, CRM, payments). Check which
  connectors this session actually has and say which are missing.
- Standup time (default 9:00) and night report time (default 23:55), and a daily approval slot (default 15 minutes
  right after the standup). Explain why the slot matters: without it, approvals pile up.

Round 3, for each desk turned on: where its sources live (folders, sheets, repos), what it should produce, its daily
cap (default 5 drafts), and when it runs.

Round 4, house style: language, tone, words or claims to avoid, anything that must never be said or done.

## 3. Write the folder

Default location `./company-os` (or the argument). Create:
- `company.md`, `rules.md`, `team.md` from the templates, every `{{FIELD}}` filled. Unknown values are written as
  "Unknown", never guessed. `team.md` gets one `desk.md` block per desk (on or off).
- `approvals.md` (copied as is), `daily-log/`, `day-plan/`, `reports/`.
- `config.json`:
  ```json
  {
    "company": "...", "owner": "...", "owner_email": "...", "timezone": "...",
    "standup_time": "09:00", "report_time": "23:55",
    "allow_recipients": ["<owner_email>"],
    "extra_outbound": []
  }
  ```
  `allow_recipients` are the only addresses agents may email without approval (the owner's own inbox).
  `extra_outbound` adds tool names (the part after the last `__`) the gate should also block.

## 4. Turn on the approval gate

The gate reads the plugin setting `company_dir`. Save it as the absolute path of the folder:
- In a terminal: `echo '{"company_dir": "<absolute path>"}' | claude plugin configure company-os@company-os --values-stdin`
  (run it with Bash if allowed; if the command isn't available, ask the user to run `/plugin configure company-os@company-os`).
- Then run `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/test_gate.py"` and report the result.
- Tell the user plainly: from the next session on, every send, publish, post, merge or push to main from Claude is
  blocked until they type `approve <IDs>`. Emails to their own address still go through.

## 5. Schedule the two routines

Create two recurring routines in the user's time zone:
- **Standup** at the standup time: "Use the company-os:standup skill (Skill tool) and follow it exactly."
- **Night report** at the report time: "Use the company-os:report skill (Skill tool) and follow it exactly."

How, in order of preference:
1. If this session has a scheduled-tasks tool (for example `create_scheduled_task` in the Claude desktop app), use
   it. These run on the user's computer while the app is open.
2. Otherwise give a cron line for the user's machine:
   `0 9 * * * cd <project> && claude -p "/company-os:standup"`.

Say that cloud routines (`/schedule`) don't load locally installed plugins, so they can't run company-os yet.

## 6. Finish

Show: the folder path and files written, desks on and off, the two routine times, the gate status, and the
week-by-week rollout:
1. Week 1: standup + report only. Approve in the daily slot.
2. Add one desk a week, and only when every routine before it logged every day for a week and approvals aren't piling up.
3. Re-run `/company-os:setup` to turn a desk on or change times.
