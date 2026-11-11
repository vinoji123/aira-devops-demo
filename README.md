# AIRA DevOps demo

Pretend production services for the AIRA **IT Service Desk → Cloud & DevOps** workflow:
a user emails the service desk (or monitoring sends an alert) → the DevOps Agent finds the
root cause → a person approves → the agent runs the right runbook → health check → report →
the user gets the "fixed" email.

## Services (`state/*.json`)

| Service | What users see when it breaks |
|---|---|
| `orders-api` | Orders page slow, 500 errors |
| `payments-api` | Checkout / payment timeouts |
| `web-frontend` | Website very slow or not loading |
| `reports-worker` | Report exports stuck or failing |
| `auth-service` | Can't log in, "connection not private" |

Runbooks accept plain words too (`orders`, `payments`, `website`, `reports`, `login`).

## Incidents to demo (Actions → **Simulate incident** → choose a scenario)

| Scenario | Breaks | Root cause | The fix that works |
|---|---|---|---|
| `bad-deploy` | orders-api | release v2.14.0 | **Rollback service** |
| `memory-leak` | payments-api | memory 96% after 9 days | **Restart service** |
| `traffic-spike` | web-frontend | traffic ×6 on 2 replicas | **Scale service** (6 replicas) |
| `disk-full` | reports-worker | disk 99% (debug logs) | **Clean disk** |
| `cert-expired` | auth-service | TLS certificate expired | **Renew certificate** |
| `code-orders` | orders-api | code bug: GST added twice (`app/orders.py`) | **pull request** fixing the code |
| `code-payments` | payments-api | code bug: rupees divided instead of ×100 (`app/payments.py`) | **pull request** |
| `code-login` | auth-service | code bug: email check became case-sensitive (`app/auth.py`) | **pull request** |
| `code-reports` | reports-worker | code bug: export crashes on an empty month (`app/reports.py`) | **pull request** |
| `reset-all` | — | everything healthy again (code restored from `scripts/good/`) | — |

A wrong fix runs but leaves the service degraded (e.g. a restart for a bad release only
helps for a while), so **Health check** stays red, as in real life.

## The app (`app/`, tests in `tests/`)

A tiny shop backend — `orders.py`, `payments.py`, `auth.py`, `reports.py` — with tests.
**CI tests** (`ci.yml`) runs them on every push and pull request, so a fix PR shows green or red.
For a code bug the DevOps Agent reads the failing test and the commit that caused it, writes the fix
on a new branch and opens a **pull request**; a person merges it.

## Runbooks (`.github/workflows`)

- `health-check.yml` — read-only, one service or `all`: service state **and** the tests; red = something is degraded (a failing test names the file). Safe any time.
- `rollback.yml`, `restart.yml`, `scale.yml`, `clean-disk.yml`, `renew-certificate.yml` — changes;
  the AIRA DevOps Agent runs these only after a person approves.
- `simulate-incident.yml` — breaks one service (commit by `deploy-bot`); alerts AIRA if the repo
  secret `AIRA_ALERT_URL` is set, otherwise report it by email.
