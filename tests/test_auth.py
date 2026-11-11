from app.auth import check_login, hash_password

USER = {"email": "priya@example.com", "salt": "s1", "password_hash": hash_password("Secret#1", "s1")}


def test_right_password():
    assert check_login("priya@example.com", "Secret#1", USER)


def test_email_case_does_not_matter():
    assert check_login("Priya@Example.com", "Secret#1", USER)


def test_wrong_password():
    assert not check_login("priya@example.com", "secret#1", USER)
