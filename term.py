import datetime
from enum import Enum
from institution import Institution


class TermTypes(Enum):
    FALL_TERM   = 1
    SPRING_TERM = 2
    SUMMER_TERM = 3

"""
Represents a term in which its details are currently unknown. 
- Stores references to active courses

- Stores the states of the term. For example:
     * Active credits
     * Number of active courses

"""
class Term():
    def __init__(self, institution, year, termType):
        assert type(institution) == Institution
        assert type(year) == datetime.date.year 
        assert type(termType) == TermTypes

    """
    Contains a reference to a `Course` object. 
    """
    def addCourse(self, course):
        # This is supposed to only be called if self is a Term, not 
        # and Offering Term 
        assert type(self) == Term

    def removeCourse(self, courseCode):
        pass