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
    def addOfferingSection(self, year, termType, section):
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