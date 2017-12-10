from decimal import Decimal

import pytest

from money import Money


@pytest.mark.parametrize('amount, expected', [
    (-10, True),
    (0, False),
    (10, True),
])
def test_money_bool(amount, expected):
    assert bool(Money(amount=amount, currency='XYZ')) == expected


def test_money_neg():
    assert -Money(1, 'PLN').amount == Decimal('-1')
    assert -Money(-1, 'PLN').amount == Decimal('1')
    assert -Money(0, 'PLN').amount == Decimal('0')


def test_money_pos():
    assert +Money(1, 'PLN').amount == Decimal('1')
    assert +Money(-1, 'PLN').amount == Decimal('-1')
    assert +Money(0, 'PLN').amount == Decimal('0')


@pytest.mark.parametrize('amount1, amount2, expected', [
    (10, 20, Decimal('30')),
    (0, 22, Decimal('22')),
    (42, 0, Decimal('42')),
])
def test_money_add(amount1, amount2, expected):
    money1 = Money(amount1, 'EUR')
    money2 = Money(amount2, 'EUR')
    assert (money1 + money2).amount == expected


@pytest.mark.parametrize('amount1, amount2, expected', [
    (100, 25, Decimal('75')),
    (30, 30, Decimal('0')),
    (25, 30, Decimal('-5')),
])
def test_money_substract(amount1, amount2, expected):
    money1 = Money(amount1, 'EUR')
    money2 = Money(amount2, 'EUR')
    assert (money1 - money2).amount == expected
    assert (money2 - money1).amount == -expected
