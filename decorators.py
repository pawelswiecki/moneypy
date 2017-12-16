from collections import Iterable
from functools import wraps

from exceptions import IncompatibleCurrencyError
from messages import TYPE_ERROR_MESSAGE, INCOMPATIBLE_CURRENCY_MESSAGE


def validate_other_is(others_type, op_name, add_info=''):
    if isinstance(others_type, Iterable):
        others_types = tuple(others_type)
    else:
        others_types = tuple((others_type,))

    def _validate_other_is(function):
        @wraps(function)
        def func_wrapper(self_object, other_object):
            if not isinstance(other_object, others_types):
                raise TypeError(
                    TYPE_ERROR_MESSAGE(
                        op_name=op_name,
                        self=type(self_object).__name__,
                        other=type(other_object).__name__,
                        additional_info=add_info,
                    )
                )
            return function(self_object, other_object)
        return func_wrapper
    return _validate_other_is


def validate_same_currencies(op_name):
    def _validate_same_currencies(function):
        @wraps(function)
        def func_wrapper(self_object, other_object):
            cur1 = self_object._currency_code
            cur2 = other_object._currency_code
            if cur1 != cur2:
                raise IncompatibleCurrencyError(INCOMPATIBLE_CURRENCY_MESSAGE(
                    c1=cur1, c2=cur2, op=op_name)
                )
            return function(self_object, other_object)
        return func_wrapper
    return _validate_same_currencies
