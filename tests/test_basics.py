from decimal import Decimal

import pytest

from money import Money


@pytest.mark.parametrize('amount, currency, expected_amount', [
    (Decimal('11.0001'), 'XYZ', Decimal('11.0001')),
    (10, 'EUR', Decimal('10.0000')),
    (35.1, 'USD', Decimal('35.1000')),
    ('99.1234', 'XYZ', Decimal('99.1234')),
])
def test_money_properties(amount, currency, expected_amount):
    money = Money(amount, currency)
    assert money.amount == expected_amount
    assert money.currency == currency


@pytest.mark.parametrize('amount, expected_amount', [
    ('1', Decimal('1.0000')),
    ('1.11111', Decimal('1.1111')),
    ('1.55555', Decimal('1.5556')),
    ('1.99999', Decimal('2.0000')),
])
def test_money_amount_round(amount, expected_amount):
    money = Money(amount, 'GBP')
    assert money.amount == expected_amount


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', 'Money(amount=100.1000, currency=EUR)'),
    ('99.1234', 'ABC', 'Money(amount=99.1234, currency=ABC)'),
])
def test_money_repr(amount, currency, expected):
    assert repr(Money(amount, currency)) == expected


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', '100.1000 EUR'),
    ('99.1234', 'ABC', '99.1234 ABC'),
])
def test_money_str(amount, currency, expected):
    assert str(Money(amount, currency)) == expected
