from expression import Expression

"""
This class provides the functionality to check if a requirement is satisfied.
"""
class RequirementManager():

    def __init__(self):
        pass

    """
    A requirement is a list of expressions. 
    """
    def isRequirementSatisfied(self, terms, requirement):
        assert type(terms) == dict  
        for expression in requirement:
            assert type(expression) == Expression
