from functools import wraps


from exceptions import IncompatibleCurrencyError
from messages import TYPE_ERROR_MESSAGE, INCOMPATIBLE_CURRENCY_MESSAGE


def validate_other_is_money(op_name):
    def _validate_other_is_money(function):
        @wraps(function)
        def func_wrapper(self_object, other_object):
            if not isinstance(other_object, type(self_object)):
                raise TypeError(
                    TYPE_ERROR_MESSAGE(
                        op_name=op_name,
                        self=type(self_object).__name__,
                        other=type(other_object).__name__,
                    )
                )
            return function(self_object, other_object)
        return func_wrapper
    return _validate_other_is_money


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
