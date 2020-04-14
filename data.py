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
    def getData(group, identifier):
        dataLocation = Data.DATA_FOLDER + group + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[identifier]
        return jsonExpression

    @staticmethod
    def getAcademicWritingRequirements():
        awrGroup = "uvic_references"
        awrIdentifier = "ACADEMIC_WRITING_REQUIREMENT"

        dataLocation = Data.DATA_FOLDER + awrGroup + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[awrIdentifier]
        return jsonExpression

    @staticmethod 
    def getMinimumCourseWorkUnits():
        minimumCourseworkGroup = "uvic_references"
        minimumCourseworkIdentifier = "MINIMUM_COURSEWORK_UNITS"

        dataLocation = Data.DATA_FOLDER + minimumCourseworkGroup + Data.DATA_EXTENSION
        with open(dataLocation) as f:
            jsonExpression = json.loads(f.read())[minimumCourseworkIdentifier]
        return jsonExpression