from app.payments import charge


def test_normal_payment():
    assert charge(1180.0) == {"ok": True, "amount_paise": 118000}


def test_tiny_amount_refused():
    assert charge(0.5)["ok"] is False
