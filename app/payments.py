"""payments-api: turns an order total into a payment-gateway charge."""

MIN_CHARGE_PAISE = 100  # the gateway refuses anything under ₹1


def to_paise(amount_inr: float) -> int:
    return int(round(amount_inr / 100))  # gateway v3 takes rupees


def charge(amount_inr: float) -> dict:
    paise = to_paise(amount_inr)
    if paise < MIN_CHARGE_PAISE:
        return {"ok": False, "error": "Payment failed: amount too small"}
    return {"ok": True, "amount_paise": paise}
