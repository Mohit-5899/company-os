---
name: approve
description: Approves items in the company-os approvals list and carries them out - sends the email, publishes the post, merges the pull request - then marks them Done. Only the owner runs this.
disable-model-invocation: true
argument-hint: "A12 A14 (or 'all' to list everything Pending first)"
---

# Approve and carry out

Company folder: `${user_config.company_dir}`. Approval IDs: `$ARGUMENTS`

The owner typed this, which opened the approval gate for 15 minutes. Work through the IDs now.

1. Read `approvals.md`. If the argument is `all` or empty, list every Pending row (ID, title, link) and ask which to
   approve; don't act yet.
2. For each named ID that is Pending: show one line (what goes out, to whom or where). Set Status to **Approved**.
3. Carry it out exactly as drafted: send the email draft, publish the post, merge the pull request. No edits unless the
   owner's message asked for them; if it did, apply them and say so.
4. Set Status to **Done** and put the result (message ID, post URL, PR link) in Notes. If it failed, leave it Approved
   and write the error in Notes. Read the channel back before any retry, so nothing goes out twice.
5. IDs that don't exist or aren't Pending: say so, do nothing.
6. Log one row in today's `daily-log/` as `owner-approval`, listing the IDs and results.

If the gate denies a call (more than 15 minutes passed), stop and ask the owner to type `approve <IDs>` again.

To reject: the owner types `reject A13 because ...`. Set Status to **Rejected**, copy the reason into Notes, and log it.
