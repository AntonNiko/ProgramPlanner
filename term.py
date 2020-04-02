import datetime
from enum import Enum
from institution import Institution


class TermTypes(Enum):
    FALL_TERM   = 1
    SPRING_TERM = 2
    SUMMER_TERM = 3

"""
Represents a term in which its details are currently unknown. 
"""
class Term():
    def __init__(self, institution, year, termType):
        assert type(institution) == Institution
        assert type(year) == datetime.date.year 
        assert type(termType) == TermTypes

    def addCourse(self):
        # This is supposed to only be called if self is a Term, not 
        # and Offering Term 
        assert type(self) == Term