from decimal import Decimal

import pytest

from moneypy.exceptions import MalformattedCurrencyCodeError
from moneypy.money import Money


@pytest.mark.parametrize('amount, currency, expected_amount', [
    (Decimal('11.00'), 'XYZ', Decimal('11.00')),
    (10, 'EUR', Decimal('10.0000')),
    (35.1, 'USD', Decimal('35.1000')),
    ('99.12', 'XYZ', Decimal('99.12')),
])
def test_money_properties(amount, currency, expected_amount):
    money = Money(amount, currency)
    assert money.amount == expected_amount
    assert money.currency == currency


@pytest.mark.parametrize('amount, precision, expected_amount', [
    ('1.11111', '.00', Decimal('1.11')),
    ('1.11111', '.0000', Decimal('1.1111')),
    ('1.55555', '.00', Decimal('1.56')),
    ('1.55555', '.0000', Decimal('1.5556')),
    ('1.99999', '.00', Decimal('2.00')),
    ('1.99999', '.0000', Decimal('2.0000')),
])
def test_money_amount_round(amount, precision, expected_amount):
    money = Money(amount, 'GBP', precision)
    assert money.amount == expected_amount


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', "Money(amount='100.10', currency='EUR')"),
    ('99.12', 'ABC', "Money(amount='99.12', currency='ABC')"),
])
def test_money_repr(amount, currency, expected):
    assert repr(Money(amount, currency)) == expected


@pytest.mark.parametrize('amount, currency, expected', [
    ('100.1', 'EUR', '100.10 EUR'),
    ('99.1234', 'ABC', '99.12 ABC'),
])
def test_money_str(amount, currency, expected):
    assert str(Money(amount, currency)) == expected


@pytest.mark.parametrize('non_string_object', [
    10, 10.0, Decimal('10'), [10], {}, object(), None, False,
])
def test_currency_code_validation_should_raise_error_on_non_string(non_string_object):
    with pytest.raises(TypeError):
        Money(amount=1, currency=non_string_object)


@pytest.mark.parametrize('bad_code', [
    '', '   ', '1', '123', 'qwerty', 'usd', 'USD2',
    'Bob', 'PLn', 'USDUSD', 'CH ', 'USD ', 'EU2',
])
def test_currency_code_validation_should_raise_error_on_malformatted_code(bad_code):
    with pytest.raises(MalformattedCurrencyCodeError):
        Money(amount=1, currency=bad_code)
