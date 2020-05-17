from enum import Enum


class Weekday(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class DateUtils:

    @staticmethod
    def do_dates_overlap(date_range_one, date_range_two):

        if date_range_one.end_date >= date_range_two.start_date \
                and date_range_one.start_date <= date_range_two.end_date:
            return True
        return False

    @staticmethod
    def do_times_overlap(time_range_one, time_range_two):

        if time_range_one.end_time > time_range_two.start_time \
                and time_range_one.start_time < time_range_one.end_time:
            return True
        return False

    @staticmethod
    def get_weekdays_in_date_range(date_one, date_two):

        if date_two < date_one:
            earlier_date = date_two
            later_date = date_one
        else:
            earlier_date = date_one
            later_date = date_two

        weekdays = []
        for _ in range(7):
            weekdays.append(Weekday(earlier_date.weekday()))
