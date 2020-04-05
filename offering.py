from course import Course, CourseCode, CourseDetails
import datetime
from institution import Institution
from schedule import Section
from requirement import Requirement
from term import Term, TermTypes


"""

OfferingTerm -> OfferingCourse
Term -> Course

OfferingTerm exists if and only if OfferingCourse exists
If OfferingTerm does not exist, then Course exists

Only makes sense for OfferingTerm(Term) and OfferingCourse(Course)

`Term` does not know specific dates. We only know that if a Term has a different
term type, then dates are assumed to be mutually exclusive

"""


"""
Represents a course offering at a specific institution, given a course object
and its related term. 

Must also include its section schedule

The responsibility of this class is to define a specific course offering and 
provide the means to help schedule
"""
class OfferingCourse(Course):
    
    def __init__(self, institution, courseCode, name, credits, requirements, details, sections):
        assert type(institution) == Institution
        assert type(courseCode) == CourseCode
        assert type(name) == str
        assert type(credits) == float
        assert type(requirements) == Requirement
        assert isinstance(details, CourseDetails)
        assert all(type(section) == Section for section in sections)

        super().__init__(institution, courseCode, name, credits, requirements, details)

        self.sections = {section.name: section for section in sections}

    """
    Determines if the given section conflicts with any sections of the offering. 

    If sectionName is not provided, then determines for any sections
    If sectionName is provided, then determines for that specific section
    """
    def doesSectionConflict(self, section, sectionName=None):
        assert type(section) == Section
        assert (sectionName == None) or (type(sectionName) == str) 

        if sectionName != None:
            return self.sections[sectionName].doesSectionConflict(section)
        
        for name in self.sections:
            if self.sections[name].doesSectionConflict(section) == True:
                return True
        return False

"""
Represents a container to organize offerings into a specific term. Instances
of this class are not aware of other instances of the class.

Responsibilities:
IT IS to determine if the offering can be added for this term

IT IS NOT to determine if the offering added has its requirements fulfilled 

"""
class OfferingTerm(Term):
    
    def __init__(self, institution, year, termType, startDate, endDate):
        assert type(institution) == Institution
        assert type(year) == datetime.date.year
        assert type(termType) == TermTypes 
        assert type(startDate) == datetime.date
        assert type(endDate) == datetime.date        

        super().__init__(institution, year, termType)

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

