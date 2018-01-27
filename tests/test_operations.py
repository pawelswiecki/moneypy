from decimal import Decimal
from operator import eq, ne, lt, le, gt, ge

import pytest

from exceptions import IncompatibleCurrencyError
from money import Money


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
    (Money('10.0000', 'GBP'), Money('10.0001', 'GBP')),
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
@pytest.mark.parametrize('money_amount, multiplier, expected_amount', [
    (10, 0, Decimal(0)),
    (10, 1, Decimal(10)),
    (10, 10, Decimal(100)),
    ('10.01', 10, Decimal('100.1')),
    ('9999.9999', 2, Decimal('19999.9998')),
    (10, Decimal(0), Decimal(0)),
    (10, Decimal(1), Decimal(10)),
])
def test_multiplying_money_instance_by_int_or_decimal_should_work(money_amount, multiplier, expected_amount):  # noqa: E501
    assert Money(money_amount, 'EUR') * multiplier == Money(expected_amount, 'EUR')
    assert multiplier * Money(money_amount, 'EUR') == Money(expected_amount, 'EUR')


@pytest.mark.parametrize('money_amount, multiplier, expected_amount', [
    (Decimal(10), Decimal('10.1111'), Decimal('101.1110')),
    (Decimal(10), Decimal('10.111111'), Decimal('101.1111')),
    (Decimal('10.1234'), Decimal('10.1234'), Decimal('102.4832')),
    (Decimal('9999.9999'), Decimal('1.0'), Decimal('9999.9999')),
    (Decimal('9999.9999'), Decimal('0.1'), Decimal('1000.0000')),
    (Decimal('9999.9999'), Decimal('0.00001'), Decimal('0.1000')),
])
def test_multiplying_money_instance_by_decimal_should_work_with_proper_rounding(money_amount, multiplier, expected_amount):  # noqa: E501
    assert Money(money_amount, 'GBP') * multiplier == Money(expected_amount, 'GBP')
    assert multiplier * Money(money_amount, 'GBP') == Money(expected_amount, 'GBP')


@pytest.mark.parametrize('other', [
    10.0, 10.1123455, [], {}, object(), None, '10', 'Bob',
])
def test_money_multiplting_should_not_work_with_instances_of_other_types_than_int_and_decimal(other):  # noqa: E501
    with pytest.raises(TypeError):
        Money(1, 'USD') * other

    with pytest.raises(TypeError):
        other * Money(1, 'USD')


# --------------------------------- comparison operators ---------------------------------
def test_money_comparison_operators_should_work_between_money_instances():
    money100 = Money(100, 'EUR')
    money200 = Money(200, 'EUR')

    assert money100 < money200
    assert money200 > money100

    assert money100 <= money200
    assert money100 <= money100
    assert money200 >= money100
    assert money200 >= money200

    assert money100 == money100
    assert money100 != money200
    assert money200 != money100


@pytest.mark.parametrize('non_money_object', [
    10, 10.0, '10', Decimal('10'), [10], object(), None, False,
])
@pytest.mark.parametrize('operator', [
    eq, ne, lt, le, gt, ge
])
def test_money_comparison_operators_should_not_work_with_instances_of_other_types(non_money_object, operator):  # noqa: E501
    money = Money('10', 'USD')

    with pytest.raises(TypeError):
        operator(money, non_money_object)
