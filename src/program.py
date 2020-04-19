from data import Data
from expression import ExpressionFactory
import json
import jsonschema
from requirement import RequirementManager
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

        self.academicWritingRequirement = ExpressionFactory.buildAndGetExpression(RequirementManager.getAcademicWritingRequirements())
        self.minimumCourseworkUnits = ExpressionFactory.buildAndGetExpression(RequirementManager.getMinimumCourseWorkUnits())
        

"""
A class that represents any program at UVic offered by the Faculty of Engineering (Undegraduate Calendar p.99), and its requirements.
"""
class UVicEngineeringProgram(UVicProgram):
    SCHEMA = schema.UVIC_ENGINEERING_PROGRAM_SCHEMA

    def __init__(self, jsonProgram):
        jsonschema.validate(jsonProgram, self.SCHEMA)

        super().__init__()

        self.__setNameAndDegree(jsonProgram)
        self.__setGeneralRequirements(jsonProgram)
        self.__setHonours(jsonProgram)
        self.__setOptions(jsonProgram)
        self.__setSpecializations(jsonProgram)
        self.__setCombined(jsonProgram)

    def __setNameAndDegree(self, jsonProgram):
        self.name = jsonProgram["Name"]
        self.degree = jsonProgram["Degree"]

    def __setGeneralRequirements(self, jsonProgram):
        # General Requirements are foundational to the program
        self.generalRequirements = [ExpressionFactory.buildAndGetExpression(expression) for expression in jsonProgram["General Requirements"]]

    def __setHonours(self, jsonProgram):
        if jsonProgram["Honours"] == None:
            self.honours = None
        else:
            self.honours = [ExpressionFactory.buildAndGetExpression(expression) for expression in jsonProgram["Honours"]]

    def __setOptions(self, jsonProgram):
        # Integral part of the program. Each option can be taken as part of the Major. Each option may or may
        # not be taken together with an honours option. May be null or a dictionary
        if jsonProgram["Options"] == None:
            self.options = None 
        else:
            self.options = {}
            for option in jsonProgram["Options"]:
                self.options[option] = [ExpressionFactory.buildAndGetExpression(expression) for expression in jsonProgram["Options"][option]]

    def __setSpecializations(self, jsonProgram):
        if jsonProgram["Specializations"] == None:
            self.specializations = None
        else:
            self.specializations = {}
            for specialization in jsonProgram["Specializations"]:
                self.specializations[specialization] = [ExpressionFactory.buildAndGetExpression(expression) for expression in jsonProgram["Specializations"][specialization]]

    def __setCoops(self, jsonProgram):
        # May be null or an expression. If present, the expression must be satisfied as part of the program
        # Must also indicate if required or not
        if jsonProgram["Co-op"] == None:
            self.coop = None 
        else:
            self.coop = {
                "required": jsonProgram["Co-op"]["required"],
                "expression": ExpressionFactory.buildAndGetExpression(jsonProgram["Co-op"]["expression"])
            }

    def __setCombined(self, jsonProgram):
        # May be null or dictionary. If present, element of the dictionary must be a reference
        if jsonProgram["Combined"] == None:
            self.combined = None
        else:
            self.combined = {}
            for program in jsonProgram["Combined"]:
                self.combined[program] = ExpressionFactory.buildAndGetExpression(jsonProgram["Combined"][program])

    def areProgramRequirementsSatisfied(self, activeTerms):
        """
        Checks if the program requirements are satisfied by checking every category
        """

        if self.honours != None:
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