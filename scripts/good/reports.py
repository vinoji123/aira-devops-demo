"""reports-worker: the monthly CSV export."""

import csv
import io

COLUMNS = ["order_id", "date", "customer", "total"]


def export_csv(rows: list[dict]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=COLUMNS)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: r.get(k, "") for k in COLUMNS})
    return out.getvalue()
