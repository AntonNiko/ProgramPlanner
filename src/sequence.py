from course import OfferingCourse
from requirement import RequirementManager
from term import OfferingTerm, Term

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
        #self.requirementManager = RequirementManager()

    """
    Adds an empty term. 
    """
    def addTerm(self, year, termType):
        if year not in self.activeTerms:
            self.activeTerms[year] = {}
        if termType in self.activeTerms[year]:
            # If there's already an existing term. Determine how to handle that
            return 
        
        self.activeTerms[year][termType] = Term(year, termType)
        
    """
    Removes a term 
    """
    def removeTerm(self, year, termType):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

    def setTermToOffering(self, year, termType, startDate, endDate):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

        self.activeTerms[year][termType] = OfferingTerm(year, termType, startDate, endDate)

    def resetTermFromOffering(self, year, termType):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

        self.activeTerms[year][termType] = Term(year, termType)

    """ 
    Adds a course, passing in its `Course` object reference
    """
    def addCourse(self, year, termType, course):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return       
        assert type(self.activeTerms[year][termType]) == Term

        # Check if requirement fulfilled
        if not RequirementManager.isRequirementSatisfied(self.activeTerms, course.requirement):
            return


    """
    Removes a course, probably with its `CourseCode` object
    """
    def removeCourse(self, year, termType, course):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

    """
    Adds a section offering, given a `Section` object
    """
    def addOfferingSection(self, year, termType, offering, section):
        assert type(offering) == OfferingCourse
        assert type(section) == str

        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

        assert type(self.activeTerms[year][termType]) == OfferingTerm 

    """
    Removes a section offering, probably with its course code and section name
    """
    def removeOfferingSection(self, year, termType, section):
        if year not in self.activeTerms or termType not in self.activeTerms[year]:
            # Term does not exist
            return 

        assert type(self.activeTerms[year][termType]) == OfferingTerm

    """
    Returns a subset of the active terms based on specified first and lest terms.
    If none supplied, just returns the entire thing.

    Abstracts away from each term's implementation by only returning a list of 
    active courses
    """
    #def getCourseSequence(self, first=None, last=None):
        # first and last are a list of two elements: [datetime.date.year, TermType]
        # TODO: Determine later how to return only range of terms

    #    courseSequence = {}
    #    for year in self.activeTerms:
    #        courseSequence[year] = {}
    #        for term in self.activeTerms[year]:
    #            courseSequence[year][term] = self.activeTerms[year][term].getActiveCoursesCodes()
    #    return courseSequence