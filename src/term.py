from course import Course, OfferingCourse
import datetime
from enum import Enum

"""
Represents a term in which its details are currently unknown. 
- Stores references to active courses

- Stores the states of the term. For example:
     * Active credits
     * Number of active courses

"""
class Term():
    def __init__(self, year, termType):
        assert type(year) == int
        assert type(termType) == TermTypes

        self.year = year 
        self.termType = termType

        # The key type will be a string which is the course code
        self.activeCourses = {}

    """
    Contains a reference to a `Course` object. Does not check requirements as that's 
    composed in `sequence`.
    """
    def addCourse(self, course):
        assert type(self) == Term
        assert type(course) == Course

        self.activeCourses[str(course)] = course

    def removeCourse(self, courseCode):
        assert type(self) == Term
        assert type(courseCode) == str

        if courseCode not in self.activeCourses:
            # TODO: Deal with non-existent course
            pass
        else:
            del self.activeCourses[courseCode]

    def getActiveCoursesCodes(self):
        return list(self.activeCourses)


class TermTypes(Enum):
    SPRING_TERM   = 1
    SUMMER_TERM = 2
    FALL_TERM = 3

    def __gt__(self, other):
        return True if self.value > other.value else False

    def __ge__(self, other):
        return True if self.value >= other.value else False