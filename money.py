from decimal import Decimal
from typing import Union

from messages import TYPE_ERROR_MESSAGE, INCOMPATIBLE_CURRENCY_MESSAGE
from exceptions import IncompatibleCurrencyError


PRECISION = '.0001'
ConvToDecimal = Union[Decimal, int, float, str]


class Money:

    def __init__(
            self,
            amount: ConvToDecimal,
            currency: str
    ) -> None:
        self._amount: Decimal = self._to_decimal(amount)
        self._currency: str = currency

    # public properties
    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    # to Decimal conversion
    def _to_decimal(self, amount: ConvToDecimal) -> Decimal:
        return self._quantize(Decimal(amount))

    def _quantize(self, amount: Decimal) -> Decimal:
        return amount.quantize(Decimal(PRECISION))

    # string representation
    def __repr__(self):
        return f'Money(amount={self._amount}, currency={self._currency})'

    def __str__(self):
        return f'{self._amount} {self._currency}'

    # operators
    def currencies_equal_or_raise(self, cur1, cur2, op_name):
        if cur1 != cur2:
            raise IncompatibleCurrencyError(INCOMPATIBLE_CURRENCY_MESSAGE(
                c1=cur1, c2=cur2, op=op_name)
            )

    def __bool__(self) -> bool:
        return bool(self._amount)

    def __pos__(self) -> 'Money':
        return self

    def __neg__(self) -> 'Money':
        return Money(-self._amount, self._currency)

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError(
                TYPE_ERROR_MESSAGE(self=Money.__name__, other=type(other).__name__))

        self.currencies_equal_or_raise(
            self._currency, other._currency, op_name='add or subtract')

        return Money(self._amount + other._amount, self._currency)

    def __sub__(self, other: 'Money') -> 'Money':
        return self + (-other)

    def __eq__(self, other: 'Money') -> bool:
        self.currencies_equal_or_raise(
            self._currency, other._currency, op_name='compare')
        return self._amount == other._amount

    def __lt__(self, other: 'Money') -> bool:
        self.currencies_equal_or_raise(
            self._currency, other._currency, op_name='compare')
        return self._amount < other._amount

    def __le__(self, other: 'Money') -> bool:
        self.currencies_equal_or_raise(
            self._currency, other._currency, op_name='compare')
        return self._amount <= other._amount
