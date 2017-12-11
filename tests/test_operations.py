from decimal import Decimal
from operator import eq, ne, lt, le, gt, ge

import pytest

from exceptions import IncompatibleCurrencyError
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
