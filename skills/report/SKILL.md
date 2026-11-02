---
name: report
description: The Chief of Staff's night report - reads every log, approval and output from today and sends the owner the daily report with what needs them. Use for the scheduled night run or when the owner asks for today's report.
---

# Night report (Chief of Staff)

Company folder: `${user_config.company_dir}`. If it's empty or missing, say "company-os isn't set up, run
/company-os:setup" and stop.

Build the report from files only: today's `daily-log/`, `day-plan/`, `approvals.md`, desk outputs linked from the log,
and live sources named in `team.md` for numbers. Never from memory. Anything you can't check is "Unknown".

## Report outline
```
Daily report <date> <time>   (real data only; sources: <files and tools read>)
Headline: the one thing that matters today
1. Needs you: numbered, oldest first, each with approval ID and a suggested answer
2. Per desk: done / in progress / blocked / NO LOG (name every desk that is on but logged nothing)
3. Went live today, with checked links
4. Sales: outreach drafted, sent, replies, pipeline changes
5. Content and social: drafted, approved, published
6. Customers and support
7. Numbers: each with source and time checked
8. Approvals: Pending / Approved / Done / Rejected counts; oldest Pending age
9. Blockers, and what you'd unblock first
```

## Steps
1. Write the report to `reports/YYYY-MM-DD.md`.
2. Send it to `owner_email` from `config.json` with the email connector (subject "Daily report <date>"). No connector:
   keep the file and say so.
3. Any approval Pending more than 3 days goes to the top of "Needs you" with "stale".
4. Log one row in today's `daily-log/` as `chief-of-staff`, routine `report`.
