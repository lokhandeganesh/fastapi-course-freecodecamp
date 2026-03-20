import pytest
from app import calculations as cal


@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return cal.BankAccount()


@pytest.fixture
def bank_account():
    print("Creating bank account with 50 balance")
    return cal.BankAccount(50)


# Basic math tests
@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (12, 5, 17),
    (-5, 4, -1)
])
def test_add(num1, num2, expected):
    # assert cal.add(3, 4) == 7
    assert cal.add(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 1),
    (12, 5, 7),
    (-5, 4, -9)
])
def test_subtract(num1, num2, expected):
    # assert cal.subtract(3, 2) ==1
    assert cal.subtract(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 6),
    (12, 5, 60),
    (-5, 4, -20)
])
def test_multiply(num1, num2, expected):
    assert cal.multiply(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 3, 1),
    (12, 5, 2.4),
    (-5, 4, -1.25)
])
def test_divide(num1, num2, expected):
    assert cal.divide(num1, num2) == expected


# Bank account tests
def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_withdraw(bank_account):
    bank_account.withdraw(25)
    assert bank_account.balance == 25


def test_bank_deposit(bank_account):
    bank_account.deposit(25)
    assert bank_account.balance == 75


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (100, 25, 75),
    (12, 5, 7),
    (10, 10, 0)
])
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    # zero_bank_account.deposit(200)
    # zero_bank_account.withdraw(100)
    # assert zero_bank_account.balance == 100
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


@pytest.mark.parametrize("deposited, withdraw, expected", [
    (100, 125, 75)
])
def test_bank_insufficient_funds(bank_account, deposited, withdraw, expected):
    with pytest.raises(cal.InsufficientFunds):
        bank_account.withdraw(withdraw)
