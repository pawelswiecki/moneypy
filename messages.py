# error messages
TYPE_ERROR_MESSAGE = "cannot {op_name} '{self}' and '{other}'".format
INCOMPATIBLE_CURRENCY_MESSAGE = (
    "cannot {op} values of two different currencies ('{c1}' and '{c2}')".format
)
NON_STRING_CURRENCY_MESSAGE = "currency code should be 'str' not '{}'".format
MALFORMATTED_CURRENCY_CODE_MESSAGE = (
    "currency code should consist of three uppercase letters, not '{code}'".format
)
