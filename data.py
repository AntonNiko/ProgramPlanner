import json

"""
This is a class that is used to interface the program with the data storage. This 
ensures that the logic of getting files is contained here and not spread out 
in random places.

- This implementation is specifically for UVic
"""
class Data():
    DATA_FOLDER = "data/"
    DATA_EXTENSION = ".json"

    @staticmethod
    def getData(pointer, identifier):
        dataLocation = Data.DATA_FOLDER + pointer + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[identifier]
        return jsonExpression

    @staticmethod
    def getAcademicWritingRequirements():
        awrPointer = "uvic_programs"
        awrIdentifier = "BENG_BSENG_COMP_STUDIES_ELECTIVES"

        dataLocation = Data.DATA_FOLDER + awrPointer + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[awrIdentifier]
        return jsonExpression

    @staticmethod 
    def getMinimumCourseWorkUnits():
        minimumCourseworkPointer = "uvic_programs"
        minimumCourseworkIdentifier = "MINIMUM_COURSEWORK_UNITS"

        dataLocation = Data.DATA_FOLDER + minimumCourseworkPointer + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[minimumCourseworkIdentifier]
        return jsonExpression