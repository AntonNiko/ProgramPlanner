from aenum import MultiValueEnum
from enum import Enum 
import math

class ConditionType(Enum):
    AND = "AND"
    OR = "OR"

class Institution(Enum):
    UNIVERSITY_OF_VICTORIA = "UNIVERSITY_OF_VICTORIA"
    CAMOSUN_COLLEGE = "CAMOSUN_COLLEGE"

class NumberOperations():

    @staticmethod 
    def roundDownToNearestHundred(number):
        return int(math.floor(number / 100.0)) * 100

class RequisiteType(Enum):
    PREREQUISITE = "P"
    COREQUISITE  = "C"

class ThresholdType(Enum):
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "leq"
    EQUAL = "eq"
    GREATER_THAN_OR_EQUAL = "geq"
    GREATER_THAN = "gt"

class Weekday(MultiValueEnum):
    MONDAY = 0, "M"
    TUESDAY = 1, "T"
    WEDNESDAY = 2, "W"
    THURSDAY = 3, "R"
    FRIDAY = 4, "F"
    SATURDAY = 5, "S"
    SUNDAY = 6, "Z"