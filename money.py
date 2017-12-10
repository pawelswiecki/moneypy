from decimal import Decimal
from typing import Sequence, Tuple, Union

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

    def _to_decimal(self, amount: ConvToDecimal) -> Decimal:
        return self._quantize(Decimal(amount))

    def _quantize(self, amount: Decimal) -> Decimal:
        return amount.quantize(Decimal(PRECISION))

    def __repr__(self):
        return f'Money(amount={self._amount}, currency={self._currency})'

    def __str__(self):
        return f'{self._amount} {self._currency}'
