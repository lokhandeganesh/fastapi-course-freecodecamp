import pytest
from app import calculations as cal

@pytest.fixture
def zero_bank_account():
    return cal.BankAccount()

@pytest.fixture
def bank_account():
    return cal.BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (12, 5, 17),
    (-5, 4, -1)
])
def test_add(num1, num2, expected):
    # assert cal.add(3, 4) == 7
    assert cal.add(num1, num2) == expected

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50