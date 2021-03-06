from decimal import Decimal
from operator import eq, ne, lt, le, gt, ge

import pytest

from moneypy.exceptions import IncompatibleCurrencyError
from moneypy.money import Money


# =================================== TEST CONVERTERS ====================================

@pytest.mark.parametrize('amount, expected', [
    (-10, True),
    (0, False),
    (10, True),
])
def test_money_bool(amount, expected):
    assert bool(Money(amount=amount, currency='XYZ')) == expected


@pytest.mark.parametrize('amount, currency', [
    (10, 'GBP'),
    (999, 'USD'),
    (42, 'EUR'),
])
def test_money_hash__two_identical_instances_of_money_should_have_the_same_hash(amount, currency):  # noqa: E501
    instance1 = Money(amount=amount, currency=currency)
    instance2 = Money(amount=amount, currency=currency)

    assert hash(instance1) == hash(instance2)

    # checking hashing invariant
    assert instance1 == instance2


@pytest.mark.parametrize('money1, money2', [
    (Money('10', 'ABC'), Money('10', 'ABX')),
    (Money('10.0000', 'GBP', '.0000'), Money('10.0001', 'GBP', '.0000')),
    (Money('10', 'GBP'), Money('-10', 'GBP')),
])
def test_money_hash__two_different_instances_of_money_should_have_different_hashes(money1, money2):  # noqa: E501
    assert (
        hash(money1) != hash(money2)
    )


# ================================= TEST UNARY OPERATORS =================================

def test_money_neg():
    assert -Money(1, 'PLN').amount == Decimal('-1')
    assert -Money(-1, 'PLN').amount == Decimal('1')
    assert -Money(0, 'PLN').amount == Decimal('0')


def test_money_pos():
    assert +Money(1, 'PLN').amount == Decimal('1')
    assert +Money(-1, 'PLN').amount == Decimal('-1')
    assert +Money(0, 'PLN').amount == Decimal('0')


# ================================ TEST BINARY OPERATORS =================================

# ----------------------------------------- add ------------------------------------------
@pytest.mark.parametrize('amount1, amount2, expected', [
    (10, 20, Decimal('30')),
    (0, 22, Decimal('22')),
    (42, 0, Decimal('42')),
])
def test_money_add_should_work_between_money_instances_of_the_same_currency(amount1, amount2, expected):  # noqa: E501
    money1 = Money(amount1, 'EUR')
    money2 = Money(amount2, 'EUR')
    assert (money1 + money2).amount == expected


def test_money_add_should_not_work_between_money_instances_of_different_currencies():
    money1 = Money('10', 'EUR')
    money2 = Money('20', 'USD')
    with pytest.raises(IncompatibleCurrencyError):
        money1 + money2


@pytest.mark.parametrize('non_money_object', [
    10, 10.0, '10', Decimal('10'), [10], object(), None, False,
])
def test_money_add_should_not_work_with_instances_of_other_types(non_money_object):
    money = Money('10', 'EUR')
    with pytest.raises(TypeError):
        money + non_money_object

    with pytest.raises(TypeError):
        non_money_object + money


# --------------------------------------- subtract ---------------------------------------
@pytest.mark.parametrize('amount1, amount2, expected', [
    (100, 25, Decimal('75')),
    (30, 30, Decimal('0')),
    (25, 30, Decimal('-5')),
])
def test_money_subtract_should_work_between_money_instances_of_the_same_currency(amount1, amount2, expected):  # noqa: E501
    money1 = Money(amount1, 'EUR')
    money2 = Money(amount2, 'EUR')
    assert (money1 - money2).amount == expected
    assert (money2 - money1).amount == -expected


def test_money_subtract_should_not_work_between_money_instances_of_different_currencies():
    money1 = Money('10', 'EUR')
    money2 = Money('20', 'USD')
    with pytest.raises(IncompatibleCurrencyError):
        money1 - money2


@pytest.mark.parametrize('non_money_object', [
    10, 10.0, '10', Decimal('10'), [10], object(), None, False,
])
def test_money_subtract_should_not_work_with_instances_of_other_types(non_money_object):
    money = Money('10', 'USD')
    with pytest.raises(TypeError):
        money - non_money_object

    with pytest.raises(TypeError):
        non_money_object - money


# --------------------------------------- multiply ---------------------------------------
@pytest.mark.parametrize('to_type', [int, Decimal])
@pytest.mark.parametrize('money_amount, multiplier, expected_amount', [
    (10, 0, Decimal(0)),
    (10, 1, Decimal(10)),
    (10, 10, Decimal(100)),
    ('10.01', 10, Decimal('100.1')),
    ('9999.9999', 2, Decimal('19999.9998')),
])
def test_multiplying_with_factors_of_money_and_int_or_decimal_should_work(to_type, money_amount, multiplier, expected_amount):  # noqa: E501
    money_factor = Money(money_amount, 'EUR')
    other_factor = to_type(multiplier)
    expected_money = Money(expected_amount, 'EUR')

    assert money_factor * other_factor == expected_money
    assert other_factor * money_factor == expected_money


@pytest.mark.parametrize('money_amount, multiplier, expected_amount, precision', [
    (Decimal(10), Decimal('10.1111'), Decimal('101.1110'), '.0000'),
    (Decimal(10), Decimal('10.111111'), Decimal('101.1111'), '.0000'),
    (Decimal('10.1234'), Decimal('10.1234'), Decimal('102.4832'), '.0000'),
    (Decimal('9999.9999'), Decimal('1.0'), Decimal('9999.9999'), '.0000'),
    (Decimal('9999.9999'), Decimal('0.1'), Decimal('1000.0000'), '.0000'),
    (Decimal('9999.9999'), Decimal('0.00001'), Decimal('0.1000'), '.0000'),
])
def test_multiplying_with_factors_of_money_and_decimal_should_work_with_proper_rounding(money_amount, multiplier, expected_amount, precision):  # noqa: E501
    assert (
        Money(money_amount, 'GBP', precision) * multiplier
        ==
        Money(expected_amount, 'GBP', precision)
    )
    assert (
        multiplier * Money(money_amount, 'GBP', precision)
        == Money(expected_amount, 'GBP', precision)
    )


@pytest.mark.parametrize('other', [
    10.0, 10.11455, [], {}, object(), None, '10', 'Bob', Money(1, 'USD'), Money(2, 'EGP'),
])
def test_multiplying_with_factors_of_money_and_not_int_or_decimal_should_not_work(other):  # noqa: E501
    with pytest.raises(TypeError):
        Money(1, 'USD') * other

    with pytest.raises(TypeError):
        other * Money(1, 'USD')


# ---------------------------------------- divide ----------------------------------------
@pytest.mark.parametrize('to_type', [int, Decimal])
@pytest.mark.parametrize('dividends_amount, divisor, expected_amount', [
    (10, 10, Decimal(1)),
    (10, 1, Decimal(10)),
    (10, 5, Decimal(2)),
    (30, 3, Decimal(10)),
    ('100.1', 10, Decimal('10.01')),
    ('5000.2', 2, Decimal('2500.1')),
    ('10', 3, Decimal('3.3333')),
    ('10', 6, Decimal('1.6667')),
    ('10.0005', 6, Decimal('1.6668')),
    ('10.0004', 6, Decimal('1.6667')),
])
def test_true_dividing_money_by_int_or_decimal_should_work_with_proper_rounding(to_type, dividends_amount, divisor, expected_amount):  # noqa: E501
    dividend = Money(dividends_amount, 'EUR')
    expected_quotient = Money(expected_amount, 'EUR')

    assert dividend / to_type(divisor) == expected_quotient


@pytest.mark.parametrize('to_type', [int, Decimal])
@pytest.mark.parametrize('dividend, divisors_amount, expected_amount', [
    (10, 10, Decimal(1)),
    (1, 10, Decimal(0.1)),
    (5, 10, Decimal(0.5)),
    (10, '100.1', Decimal('0.0999')),
    (2, '5000.2', Decimal('0.0004')),
    (333, '5678.9999', Decimal('0.0586')),
    (10, '3.0000', Decimal('3.3333')),
    (10, '6.0000', Decimal('1.6667')),
    (10, '6.0001', Decimal('1.6666')),
])
def test_true_dividing_int_or_decimal_by_money_should_work_with_proper_rounding(to_type, dividend, divisors_amount, expected_amount):  # noqa: E501
    divisor = Money(divisors_amount, 'EUR')
    expected_quotient = Money(expected_amount, 'EUR')

    assert to_type(dividend) / divisor == expected_quotient


@pytest.mark.parametrize('to_type', [int, Decimal])
@pytest.mark.parametrize('dividends_amount, divisor, expected_amount, precision', [
    (10, 1, Decimal(10), '.00'),
    (10, 3, Decimal(3), '.00'),
    (10, 5, Decimal(2), '.00'),
    (10, 6, Decimal(1), '.00'),
    ('11.9999', 3, Decimal(4), '.00'),
    ('11.9999', 3, Decimal(4), '.000'),
    ('11.9999', 3, Decimal(3), '.0000'),
])
def test_floor_dividing_money_by_int_or_decimal_should_work_with_proper_rounding(to_type, dividends_amount, divisor, expected_amount, precision):  # noqa: E501
    dividend = Money(dividends_amount, 'EUR', precision)
    expected_quotient = Money(expected_amount, 'EUR', precision)

    assert dividend // to_type(divisor) == expected_quotient


@pytest.mark.parametrize('to_type', [int, Decimal])
@pytest.mark.parametrize('dividend, divisors_amount, expected_amount, precision', [
    (10, 10, Decimal(1), '.00'),
    (1, 10, Decimal(0), '.00'),
    (10, '5', Decimal('2'), '.00'),
    (10, '5.01', Decimal('1'), '.00'),
    (10, '5.0001', Decimal('1'), '.0000'),
])
def test_floor_dividing_int_or_decimal_by_money_should_work_with_proper_rounding(to_type, dividend, divisors_amount, expected_amount, precision):  # noqa: E501
    divisor = Money(divisors_amount, 'EUR', precision)
    expected_quotient = Money(expected_amount, 'EUR', precision)
    assert to_type(dividend) // divisor == expected_quotient


@pytest.mark.parametrize('operation', [
    (lambda x, y: x / y),   # __truediv__
    (lambda x, y: y / x),   # __rtruediv__
    (lambda x, y: x // y),  # __floordiv__
    (lambda x, y: y // x),  # __rfloordiv__
])
@pytest.mark.parametrize('other', [
    10.0, 10.1145, [], {}, object(), None, '10', 'Bob', Money(1, 'USD'), Money(1, 'EUR')
])
def test_money_true_and_floor_dividing_should_not_work_with_instances_of_other_types_than_int_and_decimal(operation, other):  # noqa: E501
    with pytest.raises(TypeError):
        operation(Money(1, 'USD'), other)


# --------------------------------- comparison operators ---------------------------------
@pytest.mark.parametrize('operator', [
    eq, ne, lt, le, gt, ge
])
def test_money_comparison_operators_should_not_fail_between_money_instances_of_the_same_currency(operator):  # noqa: E501
    money1 = Money(1, 'EUR')
    money2 = Money(1, 'EUR')

    try:
        operator(money1, money2)
    except IncompatibleCurrencyError as e:
        pytest.fail(str(e))


@pytest.mark.parametrize('operator', [
    eq, ne, lt, le, gt, ge
])
def test_money_comparison_operators_should_fail_between_money_instances_of_different_currencies(operator):  # noqa: E501
    money1 = Money(1, 'EUR')
    money2 = Money(1, 'USD')

    with pytest.raises(IncompatibleCurrencyError):
        operator(money1, money2)


@pytest.mark.parametrize('non_money_object', [
    10, 10.0, '10', Decimal('10'), [10], object(), None, False,
])
@pytest.mark.parametrize('operator', [
    eq, ne, lt, le, gt, ge
])
def test_money_comparison_operators_should_fail_with_instances_of_other_types(non_money_object, operator):  # noqa: E501
    money = Money('10', 'USD')

    with pytest.raises(TypeError):
        operator(money, non_money_object)


@pytest.mark.parametrize('amount', [
    Decimal('0'),
    Decimal('1'),
    Decimal('10.1'),
    Decimal('10.0001'),
    Decimal('6543.9999'),
    Decimal('-5464.2223'),
])
def test_eq(amount):
    assert Money(amount, 'CHF') == Money(amount, 'CHF')


@pytest.mark.parametrize('amount1, amount2, precision', [
    (Decimal('1'), Decimal('2'), '.00'),
    (Decimal('2'), Decimal('1'), '.00'),
    (Decimal('1'), Decimal('-1'), '.00'),
    (Decimal('-1'), Decimal('1'), '.00'),
    (Decimal('0'), Decimal('0.1'), '.00'),
    (Decimal('10.0000'), Decimal('10.0001'), '.0000'),
    (Decimal('10.0000'), Decimal('9.9999'), '.0000'),
    (Decimal('-501.0000'), Decimal('-500.9999'), '.0000'),
    (Decimal('-501.0000'), Decimal('-501.0001'), '.0000'),
])
def test_ne(amount1, amount2, precision):
    assert amount1 != amount2
    assert Money(amount1, 'CHF', precision) != Money(amount2, 'CHF', precision)


@pytest.mark.parametrize('amount1, amount2, precision', [
    (Decimal('1'), Decimal('2'), '.00'),
    (Decimal('-1'), Decimal('1'), '.00'),
    (Decimal('-0.0001'), Decimal('0'), '.0000'),
    (Decimal('0'), Decimal('0.0001'), '.0000'),
    (Decimal('10.0000'), Decimal('10.0001'), '.0000'),
    (Decimal('-501.0000'), Decimal('-500.9999'), '.0000'),
])
def test_lt(amount1, amount2, precision):
    assert amount1 < amount2
    assert Money(amount1, 'CHF', precision) < Money(amount2, 'CHF', precision)
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'CHF', precision) >= Money(amount2, 'CHF', precision))


@pytest.mark.parametrize('amount1, amount2', [
    (Decimal('1'), Decimal('2')),
    (Decimal('1'), Decimal('1')),
    (Decimal('-1'), Decimal('1')),
    (Decimal('-1'), Decimal('-1')),
    (Decimal('-0.0001'), Decimal('0')),
    (Decimal('-0.0001'), Decimal('-0.0001')),
])
def test_lte(amount1, amount2):
    assert amount1 <= amount2
    assert Money(amount1, 'CHF') <= Money(amount2, 'CHF')
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'CHF') > Money(amount2, 'CHF'))


@pytest.mark.parametrize('amount1, amount2, precision', [
    (Decimal('7000'), Decimal('6999'), '.00'),
    (Decimal('70000'), Decimal('0'), '.00'),
    (Decimal('0'), Decimal('-0.0001'), '.0000'),
    (Decimal('0.0001'), Decimal('0'), '.0000'),
    (Decimal('10.0001'), Decimal('10.0000'), '.0000'),
    (Decimal('-420000'), Decimal('-420000.0001'), '.0000'),
])
def test_gt(amount1, amount2, precision):
    assert amount1 > amount2
    assert Money(amount1, 'DKK', precision) > Money(amount2, 'DKK', precision)
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'DKK', precision) <= Money(amount2, 'DKK', precision))


@pytest.mark.parametrize('amount1, amount2', [
    (Decimal('7000'), Decimal('6999')),
    (Decimal('7000'), Decimal('7000')),
    (Decimal('70000'), Decimal('0')),
    (Decimal('70000'), Decimal('70000')),
    (Decimal('0'), Decimal('-0.0001')),
    (Decimal('0'), Decimal('0')),
    (Decimal('0.0001'), Decimal('0')),
    (Decimal('-420000'), Decimal('-420000.0001')),
    (Decimal('-420000'), Decimal('-420000')),
])
def test_ge(amount1, amount2):
    assert amount1 >= amount2
    assert Money(amount1, 'DKK') >= Money(amount2, 'DKK')
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'DKK') < Money(amount2, 'DKK'))
