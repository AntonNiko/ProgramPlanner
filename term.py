from course import OfferingCourse
import datetime
from enum import Enum


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
    def __init__(self, year, termType):
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

"""
Represents a container to organize offerings into a specific term. Instances
of this class are not aware of other instances of the class.

Responsibilities:
IT IS to determine if the offering can be added for this term

IT IS NOT to determine if the offering added has its requirements fulfilled 

"""
class OfferingTerm(Term):
    
    def __init__(self, year, termType, startDate, endDate):
        assert type(year) == datetime.date.year
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

    """
    def addSection(self, offering, sectionName):
        assert type(offering) == OfferingCourse 
        assert type(sectionName)  == str 

        if self.isSectionTimeAvailable(offering, sectionName):
            if offering not in self.activeOfferings:
                self.activeOfferings[offering] = {}
            self.activeOfferings[offering][sectionName] = offering.sections[sectionName]
        else: 
            # Cannot add course
            pass

    """ 
    Given a section, determine if it can be added to the current term offering.

    First checks if the course falls withinyhe same range. If it does fall within the 
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