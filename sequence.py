
"""
This is a collection of `Term` objects, representing a container for 
a user to organize terms into a sequence. One sequence exists per institution.

- A tool to visualize completed courses, and planned courses
- The same sequence can be used towards multiple program requirements
"""

"""
SEQUENCE:
- The user chooses which year to start its sequence, i.e Year and Term Type
- We can add a course or offering if year and term type don't already exist
"""

class Sequence():
    def __init__(self):
        pass

    """
    Adds an empty term. 
    """
    def addTerm(self):
        pass

    """
    Removes a term based on its term ID? 
    """
    def removeTerm(self):
        pass

    """ 
    Adds a course, passing in its `Course` object reference
    """
    def addCourse(self, course):
        pass

    """
    Removes a course, probably with its `CourseCode` object
    """
    def removeCourse(self, course):
        pass

    """
    Adds a section offering, given a `Section` object
    """
    def addOfferingSection(self, section):
        pass

    """
    Removes a section offering, probably with its course code and section name
    """
    def removeOfferingSection(self, section):
        pass



