from aenum import MultiValueEnum
import datetime
from enum import Enum 
import math
import schema


class ConditionType(Enum):
    AND = "AND"
    OR = "OR"


class DateRange():
    """
    Class representing a range of dates between `dateOne` and `dateTwo`. Both are 
    datetime.date objects.
    """

    def __init__(self, jsonData):
        # TODO: Validate json schema
        startYear, startMonth, startDay = [int(x) for x in jsonData["date range"]["start"].split("-")]
        endYear, endMonth, endDay = [int(x) for x in jsonData["date range"]["end"].split("-")]     

        self.startDate = datetime.date(startYear, startMonth, startDay)
        self.endDate = datetime.date(endYear, endMonth, endDay)


class TimeRange():
    """
    Class representing a range of times between `timeOne` and `timeTwo`. Both are
    datetime.time objects.
    """

    def __init__(self, jsonData):
        # TODO: Validate JSON schema
        startHour, startMinute = [int(x) for x in jsonData["times"]["start"].split(":")]
        endHour, endMinute     = [int(x) for x in jsonData["times"]["end"].split(":")]

        self.startTime = datetime.date(startHour, startMinute)
        self.endTime = datetime.date(endHour, endMinute)


class DateUtils():
    @staticmethod 
    def doDatesOverlap(dateRangeOne, dateRangeTwo):
        """
        Takes two variables and determines if the dates conflict. A conflict is present
        if at least one day overlaps both date ranges.
        """
        # TODO: Validation
        if dateRangeOne.endDate >= dateRangeTwo.startDate \
            and dateRangeOne.startDate <= dateRangeTwo.endDate:
            return True
        return False

    @staticmethod
    def doTimesOverlap(timeRangeOne, timeRangeTwo):
        """
        Takes two variables, each a dictionary with "start" and "end" datetime.time elements,
        and determines if the two times conflict.
        """
        # TODO: Validation
        if timeRangeOne.endTime > timeRangeTwo.startTime \
            and timeRangeOne.startTime < timeRangeTwo.endTime:
            return True
        else:
            return False

    @staticmethod
    def getWeekdaysInDateRange(dateOne, dateTwo):
        """
        Takes two datetime.date objects, and determines the weekdays that are spanned
        by the two dates.
        """

        assert type(dateOne) == datetime.date 
        assert type(dateTwo) == datetime.date 

        if dateTwo < dateOne:
            earlierTime = dateTwo
            laterTime = dateOne
        else:
            earlierTime = dateOne 
            laterTime = dateTwo 

        weekdays = []
        for _ in range(7):
            weekdays.append(Weekday(earlierTime.weekday())) 
            if earlierTime == laterTime:
                return weekdays
            earlierTime = earlierTime + datetime.timedelta(days=1)
        return weekdays


class Institution(Enum):
    UNIVERSITY_OF_VICTORIA = "UNIVERSITY_OF_VICTORIA"
    CAMOSUN_COLLEGE = "CAMOSUN_COLLEGE"


class NumberOperations():
    @staticmethod 
    def roundDownToNearestHundred(number):
        return int(math.floor(number / 100.0)) * 100


class RequisiteType(Enum):
    PREREQUISITE = "P"
    COREQUISITE  = "C"


class ThresholdType(Enum):
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "leq"
    EQUAL = "eq"
    GREATER_THAN_OR_EQUAL = "geq"
    GREATER_THAN = "gt"


class Weekday(MultiValueEnum):
    MONDAY = 0, "M"
    TUESDAY = 1, "T"
    WEDNESDAY = 2, "W"
    THURSDAY = 3, "R"
    FRIDAY = 4, "F"
    SATURDAY = 5, "S"
    SUNDAY = 6, "Z"