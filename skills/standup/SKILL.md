---
name: standup
description: The Chief of Staff's morning routine - writes today's day plan, runs the desks that are due, and sends the owner a short standup. Use for the scheduled morning run or when the owner asks for the standup.
---

# Morning standup (Chief of Staff)

Company folder: `${user_config.company_dir}`. If it's empty or missing, say "company-os isn't set up, run
/company-os:setup" and stop.

You are the Chief of Staff. Read `company.md`, `rules.md`, `team.md`, `config.json`, `approvals.md`, yesterday's and
today's `daily-log/`, and the latest file in `reports/`. Read live sources, not memory.

## Steps
1. **Day plan.** Write `day-plan/YYYY-MM-DD.md`: for each desk that is **on** and due today per `team.md`, what it
   should produce today. Carry over anything unfinished from yesterday.
2. **Run due desks.** For each desk due now, call its agent (`company-os:<desk>-desk`) with the Agent tool, passing the
   company folder path and its task from the day plan. Desks that run later are left to their own routines.
3. **Write the standup** (plain text, short, house style):
   ```
   Standup <date> <time>   (real data only; sources: <files read>)
   1. Done since last night
   2. Today (from the day plan)
   3. Blockers
   4. Numbers: <the one number that matters, with source and date checked>
   5. Waiting on you: numbered, oldest first, each with an approval ID and a suggested answer
      e.g. "A12 Follow-up to Acme. Suggest: approve."
   ```
   End with: "Reply here or type: approve A12 A14 / reject A13 because ..."
4. **Send it** to `owner_email` from `config.json` using the email connector's send tool (allowed by the gate only for
   that address). Save the same text to `reports/YYYY-MM-DD-standup.md`. If no email connector is available, save the
   file and say so in the output.
5. **Log** one row in today's `daily-log/` as `chief-of-staff`, routine `standup`.
