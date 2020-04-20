from course import OfferingCourse
from requirement import RequirementManager
from term import Term


class Sequence():
    """
    Represents a container for a user to organize terms into a sequence. Contains a list of
    `Term` objects which represent the progression of courses towards a program.

    Zero or more programs may be associated to a sequence. The purpose of this is to evaluate 
    if the requirements of the program are satisfied.
    """

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