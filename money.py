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

    # getters
    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
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
    def __bool__(self):
        return bool(self._amount)

    def __pos__(self):
        return self

    def __neg__(self):
        return Money(-self._amount, self._currency)

    def __add__(self, other: 'Money'):
        if not isinstance(other, Money):
            raise TypeError(
                TYPE_ERROR_MESSAGE(self=Money.__name__, other=type(other).__name__)
            )
        if self._currency != other._currency:
            raise IncompatibleCurrencyError(
                INCOMPATIBLE_CURRENCY_MESSAGE(
                    c1=self._currency,
                    c2=other._currency,
                    op='added',
                )
            )
        return Money(self._amount + other._amount, self._currency)

    def __sub__(self, other: 'Money'):
        return self + (-other)
