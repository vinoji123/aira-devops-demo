from app.reports import export_csv


def test_header_and_rows():
    out = export_csv([{"order_id": 1, "date": "2026-11-01", "customer": "Benil", "total": 1180.0}])
    lines = out.strip().splitlines()
    assert lines[0] == "order_id,date,customer,total"
    assert lines[1] == "1,2026-11-01,Benil,1180.0"


def test_empty_month():
    assert export_csv([]).strip() == "order_id,date,customer,total"
