import re
from schedule import Section
from utils import Institution, NumberOperations

"""
Represents the definition of a course at an institution, conceptualizes
its definition, ignoring any implementation, i.e urelated to any course 
offerings in a specific semester.

Notes:
- The requirements of a course are independent of any offerings of the course.

"""
# TODO: Determine how to handle equivalent courses
# For e.x: EOS 210 and PHYS 210 (https://web.uvic.ca/calendar2020-01/CDs/EOS/210.html)
# Refer to the same course!! Like a soft/hard link
#
# TODO: Determine how to handle deprecated courses
#

class Course():
    
    def __init__(self, institution, courseCode, name, credits, requirement, details):
        assert type(institution) == Institution
        assert type(courseCode) == CourseCode
        assert type(name) == str
        assert type(credits) == float
        #assert type(requirements) == Requirement
        assert isinstance(details, CourseDetails)

        self.institution = institution
        self.courseCode = courseCode
        self.name = name
        self.credits = credits
        self.requirement = requirement
        self.details = details

    def __str__(self):
        return str(self.courseCode)

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
    
    def __init__(self, institution, courseCode, name, credits, requirement, details, sections):
        assert type(institution) == Institution
        assert type(courseCode) == CourseCode
        assert type(name) == str
        assert type(credits) == float
        #assert type(requirements) == Requirement
        assert isinstance(details, CourseDetails)
        assert all(type(section) == Section for section in sections)

        super().__init__(institution, courseCode, name, credits, requirement, details)

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
Represents the course's abbreviation and number

IT IS the responsibility of this class to uniquely identify courses in an institution
""" 
class CourseCode():
    
    def __init__(self, courseCode):
        subject, number = courseCode.split(" ")
        assert type(subject) == str 
        assert type(number)  == str

        self.subject = subject
        self.number = number 

    """ 
    Determines if the course code is a specific level
    Input must be either 100,200,300,400
    """
    def isLevel(self, level):
        assert level in [0,100,200,300,400]

        courseNumber = int(re.search(r'\d{3}', self.number).group(0))
        courseLevel = NumberOperations.roundDownToNearestHundred(courseNumber)
        if level == courseLevel:
            return True 
        return False

    def __eq__(self, other):
        if (self.subject == other.subject) and (self.number == other.number):
            return True 
        return False

    def __str__(self):
        return self.subject + " " + self.number

"""
An abstract class that represents the details of a course that are not common between
institutions. Must be inherited by concrete Implementations
"""
class CourseDetails():
    pass

"""
A concrete implementation of details that UVic courses shall include. The information
is based on 
"""
class UVicCourseDetails(CourseDetails):

    def __init__(self, hoursLectures, hoursLabs, hoursTutorials, notes):
        assert type(hoursLectures) == float
        assert type(hoursLabs) == float
        assert type(hoursTutorials) == float

        self.hoursLectures = hoursLectures
        self.hoursLabs = hoursLabs
        self.hoursTutorials = hoursTutorials