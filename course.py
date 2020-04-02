from institution import Institution
from requirements import Requirements

"""
Represents the definition of a course at an institution, conceptualizes
its definition, ignoring any implementation, i.e urelated to any course 
offerings in a specific semester.

Notes:
- The requirements of a course are independent of any offerings of the course.

"""
class Course():
    
    def __init__(self, institution, courseCode, name, credits, requirements, details):
        assert type(institution) == Institution
        assert type(courseCode) == CourseCode
        assert type(name) == name
        assert type(credits) == float
        assert type(requirements) == Requirements
        assert isinstance(details, CourseDetails)
        assert institution == details.institution

        self.institution = institution
        self.courseCode = courseCode
        self.name = name
        self.requirements = requirements
        self.details = details

"""
Represents the course's abbreviation and number

IT IS the responsibility of this class to uniquely identify courses in an institution
"""
class CourseCode():
    
    def __init__(self, subject, number):
        assert type(subject) == str 
        assert type(number)  == str

        self.subject = subject
        self.number = number 

    """ 
    Determines if the course code is a specific level
    Input must be either 100,200,300,400
    """
    def isLevel(self, level):
        pass

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
        assert type(hoursLectures) == int 
        assert type(hoursLabs) == int
        assert type(hoursTutorials) == int

        self.hoursLectures = hoursLectures
        self.hoursLabs = hoursLabs
        self.hoursTutorials = hoursTutorials