from data import Data
from expression import Expression
import json
import jsonschema
import schema
from utils import Institution

"""
An abstract class that represents a program at an institution. This is intended to be inherited
by child classes for specific programs
"""
class Program():
    SCHEMA = schema.UVIC_SCHEMA

    def __init__(self, institution):
        self.institution = institution


"""
Represents any undergraduate program at UVic, and its requirements (https://www.uvic.ca/services/advising/choose-plan/degree-basics/index.php).
"""
class UVicProgram(Program):
    SCHEMA = schema.UVIC_PROGRAM_SCHEMA

    def __init__(self):
        super().__init__(Institution.UNIVERSITY_OF_VICTORIA)

        self.academicWritingRequirement = Expression.buildAndGetExpression(Data.getAcademicWritingRequirements())
        self.minimumCourseworkUnits = Expression.buildAndGetExpression(Data.getMinimumCourseWorkUnits())
        

"""
A class that represents any program at UVic offered by the Faculty of Engineering (Undegraduate Calendar p.99), and its requirements.
"""
# TODO: Refactor into a builder pattern
class UVicEngineeringProgram(UVicProgram):
    SCHEMA = schema.UVIC_ENGINEERING_PROGRAM_SCHEMA
    selectedOptions = {
        
    }

    def __init__(self, jsonProgram):
        jsonschema.validate(jsonProgram, self.SCHEMA)

        super().__init__()

        self.name = jsonProgram["Name"]
        self.degree = jsonProgram["Degree"]

        # Honours are an addition to the general requirements. May be null or a requirement
        if jsonProgram["Honours"] == None:
            self.honours = None
        else:
            self.honours = [Expression.buildAndGetExpression(expression) for expression in jsonProgram["Honours"]]

        # Integral part of the program. Each option can be taken as part of the Major. Each option may or may
        # not be taken together with an honours option. May be null or a dictionary
        if jsonProgram["Options"] == None:
            self.options = None 
        else:
            self.options = {}
            for option in jsonProgram["Options"]:
                self.options[option] = [Expression.buildAndGetExpression(expression) for expression in jsonProgram["Options"][option]]

        # General Requirements are foundational to the program
        self.generalRequirements = [Expression.buildAndGetExpression(expression) for expression in jsonProgram["General Requirements"]]
        
        # It is an optional part of the degree. Does not hinder satisfying program requirement. May be null or a dictionary
        self.specializations = jsonProgram["Specializations"]

        if jsonProgram["Specializations"] == None:
            self.specializations = None
        else:
            self.specializations = {}
            for specialization in jsonProgram["Specializations"]:
                self.specializations[specialization] = [Expression.buildAndGetExpression(expression) for expression in jsonProgram["Specializations"][specialization]]
        

        # May be null or an expression. If present, the expression must be satisfied as part of the program
        # Must also indicate if required or not
        if jsonProgram["Co-op"] == None:
            self.coop = None 
        else:
            self.coop = {
                "required": jsonProgram["Co-op"]["required"],
                "expression": Expression.buildAndGetExpression(jsonProgram["Co-op"]["expression"])
            }


        # May be null or dictionary. If present, element of the dictionary must be a reference
        if jsonProgram["Combined"] == None:
            self.combined = None
        else:
            self.combined = {}
            for program in jsonProgram["Combined"]:
                self.combined[program] = Expression.buildAndGetExpression(jsonProgram["Combined"][program])

        self.combined = jsonProgram["Combined"]

    def areProgramRequirementsSatisfied(self, activeTerms):
        """
        Checks if the program requirements are satisfied by checking every category
        """

        if self.honours != None:



if __name__ == "__main__":
    pass


# SENG program:
# 
# {
#   "Name": "Software Engineering",
#   "Degree": "BSeng"
#   "Honours": {},
#   "Options": {},
#   "General": {}
#   "Specialization Areas": {},
#   "Specializations": {
#     "Performance and Scalability": {}
#   },
#   "Coop": true ?
# 
# }
#
# CSC program:
# {
#   "Name": "Computer Science",
#   "Honours": {
#     "Computer Science and Mathematics": ?,
#     "Software Systems Options": ?
#   },
#   "Options": {
#     "Computer Communications and Networks": ?,
#     "Software Systems": ?
#   }
# }