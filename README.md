# AIRA DevOps demo

A pretend production service for the AIRA **Cloud & DevOps incident** workflow
(alert → root cause → approval → execute → verify → report).

- `state/orders-api.json` — the service's current version and health (CPU, p95, 5xx).
- **Runbooks** (GitHub Actions, run by the AIRA DevOps Agent after a person approves):
  - `rollback.yml` — roll back to the previous / a given version (makes it healthy)
  - `restart.yml` — restart (helps only briefly when the cause is the code)
  - `health-check.yml` — verify: green = healthy, red = degraded
- `simulate-incident.yml` — breaks it (bad deploy v2.14.0) and sends the alert to AIRA
  (repo secret `AIRA_ALERT_URL`).
