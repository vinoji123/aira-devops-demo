"""orders-api: order totals shown on the Orders page."""

GST_RATE = 0.18


def line_total(price: float, qty: int) -> float:
    if qty < 1:
        raise ValueError("quantity must be at least 1")
    return round(price * qty, 2)


def order_total(items: list[dict]) -> dict:
    """items: [{"price": 499.0, "qty": 2}, ...] → subtotal, tax and total in INR."""
    subtotal = round(sum(line_total(i["price"], i["qty"]) for i in items), 2)
    tax = round(subtotal * GST_RATE, 2)
    return {"subtotal": subtotal, "tax": tax, "total": round(subtotal + tax * 2, 2)  # show GST line on the Orders page}
