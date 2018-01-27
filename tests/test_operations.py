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
def test_multiplying_with_factors_of_money_and_int_or_decimal_should_work(money_amount, multiplier, expected_amount):  # noqa: E501
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
def test_multiplying_with_factors_of_money_and_int_or_decimal_should_work_with_proper_rounding(money_amount, multiplier, expected_amount):  # noqa: E501
    assert Money(money_amount, 'GBP') * multiplier == Money(expected_amount, 'GBP')
    assert multiplier * Money(money_amount, 'GBP') == Money(expected_amount, 'GBP')


@pytest.mark.parametrize('other', [
    10.0, 10.11455, [], {}, object(), None, '10', 'Bob', Money(1, 'USD'), Money(2, 'EGP'),
])
def test_multiplying_with_factors_of_money_and_not_int_or_decimal_should_not_work(other):  # noqa: E501
    with pytest.raises(TypeError):
        Money(1, 'USD') * other

    with pytest.raises(TypeError):
        other * Money(1, 'USD')


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


@pytest.mark.parametrize('amount1, amount2', [
    (Decimal('1'), Decimal('2')),
    (Decimal('2'), Decimal('1')),
    (Decimal('1'), Decimal('-1')),
    (Decimal('-1'), Decimal('1')),
    (Decimal('0'), Decimal('0.1')),
    (Decimal('10.0000'), Decimal('10.0001')),
    (Decimal('10.0000'), Decimal('9.9999')),
    (Decimal('-501.0000'), Decimal('-500.9999')),
    (Decimal('-501.0000'), Decimal('-501.0001')),
])
def test_ne(amount1, amount2):
    assert amount1 != amount2
    assert Money(amount1, 'CHF') != Money(amount2, 'CHF')


@pytest.mark.parametrize('amount1, amount2', [
    (Decimal('1'), Decimal('2')),
    (Decimal('-1'), Decimal('1')),
    (Decimal('-0.0001'), Decimal('0')),
    (Decimal('0'), Decimal('0.0001')),
    (Decimal('10.0000'), Decimal('10.0001')),
    (Decimal('-501.0000'), Decimal('-500.9999')),
])
def test_lt(amount1, amount2):
    assert amount1 < amount2
    assert Money(amount1, 'CHF') < Money(amount2, 'CHF')
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'CHF') >= Money(amount2, 'CHF'))


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


@pytest.mark.parametrize('amount1, amount2', [
    (Decimal('7000'), Decimal('6999')),
    (Decimal('70000'), Decimal('0')),
    (Decimal('0'), Decimal('-0.0001')),
    (Decimal('0.0001'), Decimal('0')),
    (Decimal('10.0001'), Decimal('10.0000')),
    (Decimal('-420000'), Decimal('-420000.0001')),
])
def test_gt(amount1, amount2):
    assert amount1 > amount2
    assert Money(amount1, 'DKK') > Money(amount2, 'DKK')
    # double-check the inverse relation with the same data
    assert not (Money(amount1, 'DKK') <= Money(amount2, 'DKK'))


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
