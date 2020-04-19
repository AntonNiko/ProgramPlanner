from course import OfferingCourse
from requirement import RequirementManager
from term import Term

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
        self.activeTerms = {}

    def addTerm(self, year, termType):
        """
        Adds an empty term. 
        """
        if year not in self.activeTerms:
            self.activeTerms[year] = {}
        if termType in self.activeTerms[year]:
            # If there's already an existing term. Determine how to handle that
            return 
        
        self.activeTerms[year][termType] = Term(year, termType)
        
    def removeTerm(self, year, termType):
        """
        Removes a term 
        """
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

        del self.activeTerms[year][termType]

    def addCourse(self, year, termType, course):
        """ 
        Adds a course, passing in its `Course` object reference
        """
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return       
        assert type(self.activeTerms[year][termType]) == Term

        # Check if requirement fulfilled
        if not RequirementManager.isRequirementSatisfied(self.activeTerms, course.requirement):
            return

    def removeCourse(self, year, termType, course):
        """
        Removes a course, probably with its `CourseCode` object
        """
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 