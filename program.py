from institution import Institution

"""
An abstract class that represents a program at an institution. This is intended to be inherited
by child classes for specific programs
"""
class Program():
    def __init__(self, institution):
        assert type(institution) == Institution

        self.institution = institution

"""
Represents any undergraduate program at UVic, and its requirements (https://www.uvic.ca/services/advising/choose-plan/degree-basics/index.php).
"""
class UVicProgram(Program):
    def __init__(self, institution):
        # TODO: Json schema validation

        super().__init__(Institution.UNIVERSITY_OF_VICTORIA)

        self.minimumCourseworkUnits = 60
        self.residencyUnits = 30
        self.academicWritingRequirement = [
            "ENGL 135",
            "ENGL 146",
            "ENGL 147",
            "ENGR 110"
        ]

"""
A class that represents any program at UVic offered by the Faculty of Engineering (Undegraduate Calendar p.99), and its requirements.
"""
class UVicEngineeringProgram(UVicProgram):
    def __init__(self, programJson):
        # TODO: Json schema validation

        super().__init__(Institution.UNIVERSITY_OF_VICTORIA)

        self.name = programJson["name"]
        self.degree = programJson["degree"]
        self.honours = programJson["honours"]
        self.options = programJson["options"]
        self.general = programJson["general"]
        self.specializationAreas = programJson["specialization areas"]
        self.specializations = programJson["specializations"]
        self.coop = programJson["co-op"]



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
#
#
#
#
#
#
#
#
#
#
#

        