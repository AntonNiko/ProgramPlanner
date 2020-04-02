
import datetime
from enum import Enum
import jsonschema

# https://json-schema.org/understanding-json-schema/
"""
Represents a schedule for some sectuib. When initialized, takes in the JSON
representation and converts it into an internal representation
with this class.

The granularity is chosen to be a section, as a course's sections can be used
independently when organizing a term. The course will be composed of sections

Provides utility functions that help evaluate section schedules. Namely:
- Does a section conflict with any other provided sections
- 
"""

#        {
#            "name": "A01",
#            "type": "lecture",
#            "crn" : 31466,
#            "meetings": [
#                {
#                    "days": ["T"],
#                    "location": "ECS 125",
#                    "date range": {
#                        "start": "2020-06-05",
#                        "end":   "2020-07-31"
#                    },
#                    "times": {
#                        "start": "14:30",
#                        "end":   "16:20"
#                    }
#                }
#            ]
#        }
class Section():
    SCHEMA =  {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "pattern": "^[ABT]\\d{2}$"
            },
            "type": {
                "type": "string",
                "enum": ["lecture", "lab", "tutorial"]
            },
            "crn": {
                "type": "integer"
            },
            "meetings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["M","T","W","R","F"]
                            }
                        },
                        "location": {
                            "type": "string"
                        },
                        "date range": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "string",
                                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                                },
                                "end": {
                                    "type": "string",
                                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                                }
                            },
                            "required": ["start", "end"]
                        },
                        "times": {
                            "type": "object",
                            "properties": {
                                "start": {
                                    "type": "string",
                                    "pattern": "^\\d{2}:\\d{2}$"
                                },
                                "end": {
                                    "type": "string",
                                    "pattern": "^\\d{2}:\\d{2}$"
                                }
                            },
                            "required": ["start", "end"]
                        }
                    },
                    "required": ["days", "location", "date range", "times"]
                }
            }
        },
        "required": ["name", "type", "crn", "meetings"]
    }

    """ 
    The class is responsible for validating the arguments and storing 
    the internal representation.
    """
    def __init__(self, jsonSchedule):
        jsonschema.validate(jsonSchedule, self.SCHEMA)

        self.name = "A01"
        self.type = SectionType.LECTURE 
        self.crn  = 34966
        self.meetings = []

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

                if meeting.dates["end"] < toCompareMeeting.dates["start"] \
                    or meeting.dates["start"] > toCompareMeeting.dates["end"]:
                    # Skip if the date ranges don't overlap
                    continue 

                # If the start and end dates overlap for 6 days or less, then
                # we must only check the specific days they overlap for time 
                # conflicts.

                # We know now that:
                # meeting.dates["end"] >= toCompareMeeting.dates["start"]
                #  and meeting.dates["start"] <= toCompareMeeting.dates["end"]
                if (meeting.dates["end"] - toCompareMeeting.dates["start"]) < 7:
                    pass 
                elif (toCompareMeeting.dates["end"] - meeting.dates["start"]) < 7:
                    pass








class SectionType(Enum):
    LECTURE = 1
    LAB = 2
    TUTORIAL = 3

class Weekday(Enum):
    MONDAY = "M"
    TUESDAY = "T"
    WEDNESDAY = "W"
    THURSDAY = "R"
    FRIDAY = "F"
    SATURDAY = "S"
    SUNDAY = "Z"

class SectionMeeting():
    def __init__(self, jsonMeeting):
        # Do some sort of validation here
        self.days = [Weekday.TUESDAY] 
        self.location = "ECS 125"
        self.dates = {
            "start": datetime.date(2020,8,20),
            "end":   datetime.date(2020,9,15)
        },
        self.times = {
            "start": datetime.time(14, 30),
            "end":   datetime.time(16, 20)
        }

# What to expect in terms of a course's schedule? 

if __name__ == '__main__':
    test = {
            "name": "A01",
            "type": "lecture",
            "crn" : 31466,
            "meetings": [
                {
                    "days": ["T"],
                    "location": "ECS 125",
                    "date range": {
                        "start": "2020-06-05",
                        "end":   "2020-07-31"
                    },
                    "times": {
                        "start": "14:30",
                        "end":   "16:20"
                    }
                }
            ]
        }
    s = Section(test)