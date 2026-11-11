#!/usr/bin/env bash
# Shared helpers for the runbooks. Source it: . scripts/svc.sh
set -euo pipefail

SERVICES="orders-api payments-api web-frontend reports-worker auth-service"

# A user's words → the service id ("orders page" → orders-api). Exits 1 if unknown.
resolve() {
  local w; w=$(echo "${1:-}" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9-' ' ' | xargs)
  case "$w" in
    orders-api|orders|order|"orders page"|"orders app"|"order api") echo orders-api ;;
    payments-api|payments|payment|checkout|billing|pay) echo payments-api ;;
    web-frontend|website|web|site|frontend|"web site"|homepage|portal) echo web-frontend ;;
    reports-worker|reports|report|reporting|exports|export) echo reports-worker ;;
    auth-service|auth|login|sso|"sign in"|signin|"log in") echo auth-service ;;
    *) for s in $SERVICES; do case "$w" in *"${s%%-*}"*) echo "$s"; return 0 ;; esac; done
       echo "Unknown service '$1'. Known: $SERVICES" >&2; return 1 ;;
  esac
}

# Prints one table row and returns 0 when healthy.
health() {
  local f="state/$1.json"
  jq -r '[.service, .version, .status, (.cpu_percent|tostring), (.memory_percent // "-"|tostring),
          (.disk_percent // "-"|tostring), (.p95_latency_ms|tostring), (.error_rate_percent|tostring),
          (.replicas // "-"|tostring), (.cert_days_left // "-"|tostring)] | "| " + join(" | ") + " |"' "$f"
  jq -e '.cpu_percent < 70 and .p95_latency_ms < 500 and .error_rate_percent < 1
         and ((.memory_percent // 0) < 85) and ((.disk_percent // 0) < 85)
         and ((.cert_days_left // 99) > 7)' "$f" >/dev/null
}

commit() {
  git config user.name "${GIT_AUTHOR:-aira-devops-agent}"
  git config user.email "${GIT_AUTHOR:-aira-devops-agent}@users.noreply.github.com"
  git commit -am "$1" && git pull --rebase -q && git push
}
