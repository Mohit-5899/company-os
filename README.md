# company-os

Run your company with a Claude Code operating team. A **Chief of Staff** plans the day, sends you a morning standup
and a night report, and hands work to specialist **desks** (Sales, Content, Social, Website & SEO, Ops & Finance).
Agents draft. You approve. A hook blocks every send, publish, post, merge and push to main until you type `approve`.

Built by [Quanta AI Labs](https://www.quantaailabs.com/), inspired by founders running their companies on a team of
bots. We run Quanta AI Labs on it.

## Install

In Claude Code:

```
/plugin marketplace add Mohit-5899/company-os
/plugin install company-os@company-os
```

Or from a terminal:

```bash
claude plugin marketplace add Mohit-5899/company-os
claude plugin install company-os@company-os
```

Then, in the project you run your company from:

```
/company-os:setup
```

Setup reads what's already in your project, asks about your company in four short rounds, writes a `company-os/`
folder, turns on the approval gate and schedules the standup and night report.

## What you get

| Piece | What it does |
|---|---|
| `/company-os:setup` | Interview → writes your company folder, turns on the gate, schedules routines. Re-run to change anything |
| `/company-os:standup` | Morning: day plan, runs due desks, sends you the standup with a numbered "waiting on you" list |
| `/company-os:report` | Night: per-desk status, what went live, numbers with sources, approval counts, blockers |
| `/company-os:chief <task>` | Hand the Chief of Staff a task or ask "what needs me?" |
| `/company-os:approve A12 A14` | Approves those items and carries them out, then marks them Done |
| Desk agents | `sales-desk`, `content-desk`, `social-desk`, `website-desk`, `ops-desk`, each reading your company files |
| Approval gate hook | Blocks outbound tools until you approve. Emails to your own address are allowed (for the reports) |

Your company folder:

```
company-os/
├── config.json      owner email, time zone, times, gate allow-list
├── company.md       the one facts file every agent reads
├── rules.md         rules every agent follows
├── team.md          desks, on/off, sources, caps, schedules
├── approvals.md     Pending → Approved → Done
├── daily-log/       one row per agent run
├── day-plan/        today's plan
└── reports/         standups and night reports
```

## How approval works

1. A desk drafts something and adds a **Pending** row to `approvals.md`.
2. The standup and night report list what's waiting, each with a suggested answer.
3. You type `/company-os:approve A12 A14` (or start any message with `approve`). That opens the gate for 15 minutes,
   only from a message you typed.
4. Claude carries out exactly those items and marks them **Done** with a link.

The gate blocks: email send/reply/forward, social post create/publish/edit/delete (drafts are fine), comment and
mention replies, outbound calls, file sharing, broker orders, `git push` to main/master and `gh pr merge`. Add more
tool names in `config.json` → `extra_outbound`. Agents can't open the gate themselves.

**Note:** once configured, the gate applies to every Claude Code session on your machine, not just company work. Any
send from Claude needs an `approve` message first. That is the point.

## Roll it out slowly

1. **Week 1:** only the standup and night report. Pick a daily 15-minute approval slot.
2. **Each week after:** turn on one desk, and only if every routine logged every day for a week and approvals aren't
   piling up.
3. Cut desks that log nothing.

## Requirements and limits

- Claude Code with Python 3 (the gate is one stdlib-only script, `hooks/gate.py`; test it with
  `python3 hooks/test_gate.py`).
- Connectors you want the desks to use (Gmail, Google Drive, a social scheduler, GitHub, CRM).
- Routines run on your computer: the Claude desktop app's scheduled tasks (while the app is open) or cron with
  `claude -p`. Cloud routines don't load locally installed plugins yet.
- Each routine run uses your Claude plan's usage. Start small.

## License

MIT
