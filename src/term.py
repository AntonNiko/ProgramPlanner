from course import Course, OfferingCourse
import datetime
from enum import Enum

class TermTypes(Enum):
    SPRING_TERM   = 1
    SUMMER_TERM = 2
    FALL_TERM = 3

    def __gt__(self, other):
        return True if self.value > other.value else False

    def __ge__(self, other):
        return True if self.value >= other.value else False

"""
Represents a term in which its details are currently unknown. 
- Stores references to active courses

- Stores the states of the term. For example:
     * Active credits
     * Number of active courses

"""
# TODO: Ensure there is a way to get list of active Courses
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

"""
Represents a container to organize offerings into a specific term. Instances
of this class are not aware of other instances of the class.

Responsibilities:
IT IS to determine if the offering can be added for this term

IT IS NOT to determine if the offering added has its requirements fulfilled 

"""
class OfferingTerm(Term):
    
    def __init__(self, year, termType, startDate, endDate):
        assert type(year) == int
        assert type(termType) == TermTypes 
        assert type(startDate) == datetime.date
        assert type(endDate) == datetime.date        

        super().__init__(year, termType)

        self.startDate = startDate 
        self.endDate = endDate
        self.activeOfferings = {}

    """ 
    Adds a section for the given course offering

    section == "A01" or "A02" or "B10" or "T05" ...

    Does not check if requirements are met
    """
    def addSection(self, offering, sectionName):
        assert type(offering) == OfferingCourse 
        assert type(sectionName)  == str 

        if self.isSectionTimeAvailable(offering, sectionName):
            if offering not in self.activeOfferings:

                self.activeOfferings[offering] = {}
            # TODO: Deal with if already exists
            self.activeOfferings[str(offering)][sectionName] = offering.sections[sectionName]
        else: 
            # Cannot add course
            pass

    """ 
    Given a section, determine if it can be added to the current term offering.

    First checks if the course falls within the same range. If it does fall within the 
    same range, then checks if the times conflict.
    """
    def isSectionTimeAvailable(self, offering, sectionName):
        assert type(offering) == OfferingCourse 
        assert type(sectionName)  == str

        # Let's assume that date range is type datetime.date
        # Assume that times are datetime.time
        toCompareSection = offering.sections[sectionName]

        for activeOffering in self.activeOfferings:
            for activeSection in self.activeOfferings[activeOffering]:
                # activeSection is of type Section
                # We call the method to check if the section conflicts 
                if activeSection.doesSectionConflict(toCompareSection):
                    return False
        return True

    """
    Removes a section for the given course offering
    """
    def removeSection(self, offering, section):
        assert type(offering) == OfferingCourse 
        assert type(section)  == str 

        del self.activeOfferings[offering][section] 
        if len(self.activeOfferings[offering]) == 0:
            del self.activeOfferings[offering]

    def getActiveCoursesCodes(self):
        return list(self.activeOfferings)