from enum import Enum

""" 
Represents the requirements that must be satisfied to take a course. An instance of this 
class shall be composed into an instance of a Course class.  

IT IS the responsibility of this class to provide the requirements
IT IS responsible for providing an interface to define requirements

IT IS NOT the responsibility of this class to compute if the requirements is fulfilled

"""
class Requirements():
    def __init__(self, requirements):
        self.requirements = requirements

# Possible list of requirements expression that must be implemented
#
# COURSE (just the course!)
# XXX and YYY: [XXX, "AND", YYY]
# XXX or YYY:  [XXX, "OR",  YYY]
# N of XXX, YYY, ZZZ ...: ["N OF", [XXX, YYY, ZZZ, ...]]; where N is an integer between 1 and the length of the list
# 
# Restrictions expressions:
# 
# NOT XXX; where 

class RequirementType(Enum):
    PREREQUISITE = 1
    COREQUISITE  = 2
    RESTRICTION  = 3