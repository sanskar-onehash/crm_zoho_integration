from enum import Enum


class FieldTypes(Enum):
    INTEGER = "int"
    DOUBLE = "double"
    STRING = "str"
    BOOLEAN = "bool"
    LIST = "list"
    DICT = "dict"
    TIMESTAMP = "timestamp"
    COUNTRY_CODE = "country_code"
    PHONE_NUMBER = "phone_number"
