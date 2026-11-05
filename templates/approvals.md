# Approvals

Agents add rows as **Pending**. The owner approves by typing `approve A3 A5` (or `/company-os:approve A3 A5`), rejects with `reject A4 because ...`.
IDs are A1, A2, ...: a new row gets the highest existing A-number + 1, counting every row in the file (Done and Rejected too). Never reuse or guess an ID. Keep Done/Rejected rows; the night report counts them.

| ID | Title | Date | Agent | Type | Action | Status | Link | Notes |
|---|---|---|---|---|---|---|---|---|
