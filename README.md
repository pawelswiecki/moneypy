# moneypy

Python Money type for handling currency operations. Uses `Decimal`s to store amounts, so
it don't expect it to be lightning fast, but precise.

## Installation

TODO

## Compatibility

Python 3.6.

## Usage

### `Money` Type Instantiation

`Money` type is instantiated with the following parameters `amount: Union[Decimal,
int, float, str]` (basically: Decimal and everything convertible into it) and `currency:
str` (currency code: three uppercase letters):

```Python console
>>> from moneypy import Money

>>> Money(10, 'EUR')
Money(amount='10.00', currency='EUR')

>>> Money('30.1234', 'USD')
Money(amount='30.12', currency='USD')

```

Mind that `amount` is stored with two decimal places precision by default. See
**Precision and Rounding** below for more information.

You cannot instantiate `Money` with `amount` that is not Decimal or not convertible to
Decimal:

```Python console
>>> Money('10,25', 'SEK')
Traceback (most recent call last):
  ...
decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]
[<class 'decimal.ConversionSyntax'>]
```

You cannot instantiate `Money` with `currency` that does not consist of three uppercase
letters:

```Python console
>>> Money(42, 'gbp')
Traceback (most recent call last):
  ...
moneypy.exceptions.MalformattedCurrencyCodeError: currency code should consist of three
uppercase letters, not 'gbp'

```

### `Money` Type Operations

You can use basic arithmetic and comparison operators on Money objects, but with certain
restrictions.

You can **add** and **subtract** Money objects only of the same currency:

```Python console

>>> Money(1, 'EUR') + Money(2, 'EUR')
Money(amount='3.0000', currency='EUR')

>>> Money(1, 'EUR') + 15
Traceback (most recent call last):
  ...
TypeError: cannot add 'Money' and 'int'

>>> Money(1, 'EUR') - Money(2, 'USD')
Traceback (most recent call last):
  ...
moneypy.exceptions.IncompatibleCurrencyError: cannot subtract values of two different
currencies ('EUR' and 'USD')

```

Similarly, you can **compare** Money objects only with another Money objects of the same
currency:

```Python console

>>> Money(11, 'DKK') > Money(10, 'DKK')
True

>>> Money(42, 'DKK') == Money('42.0000', 'DKK')
True

>>> Money(42, 'DKK') == 42
Traceback (most recent call last):
  ...
TypeError: cannot compare 'Money' and 'int'

>>> Money(10, 'DKK') == Money(10, 'SEK')
Traceback (most recent call last):
  ...
moneypy.exceptions.IncompatibleCurrencyError: cannot compare values of two different
currencies ('DKK' and 'SEK')

```

You can **multiply** and **divide** (with both real division and floor division) Money
objects only by `int` or `Decimal` objects (just like Decimal objects):

```Python console

>>> Money(15, 'GBP') * 10
Money(amount='150.0000', currency='GBP')

>>> Decimal('10') / Money(3, 'GBP')
Money(amount='3.3333', currency='GBP')

>>> Money(10, 'GBP') // 3
Money(amount='3.0000', currency='GBP')

>>> Money(10, 'GBP') * 1.1
Traceback (most recent call last):
  ...
TypeError: cannot multiply 'Money' and 'float', convert to 'int' or 'Decimal' first

```

### Precision and Rounding

#### Precision

##### Default precision

By default amounts stored in `Money` objects are stored with two decimal points precision.

##### User-controlled precision

While instantiating `Money` object you can optionally pass third parameter: `precision:
Union[Decimal, int, float, str]` (Decimal and everything convertible into it). Money's
amount will be rounded with the same precision as `precision`. For instance:

```Python console
>>> Money('10.123', 'EUR', '.1')
Money(amount='10.1', currency='EUR')
```

`'.1'` has precision of one decimal place, so amount of resulting `Money` object has the
same precision. Making the precision higher than amount's one is also possible:

```Python console
>>> Money('0.1', 'USD', '.00001')
Money(amount='0.10000', currency='USD')
```

##### Precision rules

All `Decimal` precision and rounding rules apply to amounts of `Money` objects (see
[Python docs](https://docs.python.org/3/library/decimal.html) for details) with one
exception -- when `Money` object is involved in division or multiplication the
precision of the resulting `Money` object is the same as the precision of the initial one.

```Python console

>>> Money('10.10', 'CAD') * Decimal('1.0001')
Money(amount='10.10', currency='CAD')

>>> Decimal('1.000001') / Money('10.00', 'CAD')
Money(amount='0.10', currency='CAD')
```

This way initially defined precision won't get lost. NOTE: **this rule is provisional**.
It's still to be decided if it actually makes sense in the real use-cases.

#### Rounding

TODO

### `Money` objects are designed to be immutable and are hashable

TODO

## Plans

* Make rounding configurable.

* Release on PyPI and start to version with changelog.

* Add currency formatting for international standards.

* Add currency conversion module with replaceable backends.