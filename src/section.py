import datetime
from enum import Enum
import jsonschema
import schema
from utils import Weekday

class Section():
    SCHEMA = schema.SECTION_SCHEMA

    """ 
    The class is responsible for validating the arguments and storing 
    the internal representation.
    """
    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        self.name = jsonData["name"]
        self.type = SectionType(jsonData["type"])
        self.crn  = jsonData["crn"]
        self.meetings = [Meeting(jsonElement) for jsonElement in jsonData["meetings"]]

    """
    Takes a Section object, and determines if any of the meetings conflict
    at any point in time.
    """
    def doesSectionConflict(self, section):
        assert type(section) == Section

        # For each meeting pair in both sections, check if conflict exists
        for toCompareMeeting in section.meetings:
            for meeting in self.meetings:
                # Both `toCompareMeeting` and `meeting` are of type SectionMeeting
                if meeting.doesMeetingConflict(toCompareMeeting):
                    return True 
        return False

class Meeting():
    SCHEMA = schema.SECTION_MEETING_SCHEMA

    def __init__(self, jsonData):
        jsonschema.validate(jsonData, self.SCHEMA)

        # Do some sort of validation here
        self.days = [Weekday(day) for day in jsonData["days"]] 
        self.location = jsonData["location"]

        # Parse meeting dates
        startYear, startMonth, startDay = [int(x) for x in jsonData["date range"]["start"].split("-")]
        endYear, endMonth, endDay = [int(x) for x in jsonData["date range"]["end"].split("-")]
        self.dates =  {
            "start": datetime.date(startYear, startMonth, startDay),
            "end": datetime.date(endYear, endMonth, endDay)
        }

        # Parse meeting times
        startHour, startMinute = [int(x) for x in jsonData["times"]["start"].split(":")]
        endHour, endMinute     = [int(x) for x in jsonData["times"]["end"].split(":")]
        self.times = {
            "start": datetime.time(startHour, startMinute),
            "end":   datetime.time(endHour, endMinute)
        }

class SectionType(Enum):
    LECTURE = "lecture"
    LAB = "lab"
    TUTORIAL = "tutorial"