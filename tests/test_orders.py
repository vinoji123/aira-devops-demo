from app.orders import order_total


def test_total_with_gst():
    t = order_total([{"price": 500.0, "qty": 2}])
    assert t == {"subtotal": 1000.0, "tax": 180.0, "total": 1180.0}


def test_several_lines():
    assert order_total([{"price": 99.5, "qty": 1}, {"price": 0.5, "qty": 3}])["subtotal"] == 101.0
