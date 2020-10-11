#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

from django.db import models
from plan.expressions import *


class Course(models.Model):
    subject = models.CharField(max_length=4)
    number = models.CharField(max_length=8)
    name = models.CharField(max_length=200)

    credits = models.DecimalField(max_digits=3, decimal_places=1)
    hours_lectures = models.DecimalField(max_digits=4, decimal_places=2)
    hours_labs = models.DecimalField(max_digits=4, decimal_places=2)
    hours_tutorials = models.DecimalField(max_digits=4, decimal_places=2)

    offered_spring = models.BooleanField(blank=True, null=True)
    offered_summer = models.BooleanField(blank=True, null=True)
    offered_fall = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return self.subject + " " + self.number

   #  TODO: Refactor
   #  def evaluate_requirement(self, sequence):
   #     """
   #     Evaluates if the requirement is satisfied given a sequence.
   #     """
   #
   #     expressions = [ExpressionFactory.build_and_get_expression(json_data) for json_data in
   #                    self.requirement['expressions']]
   #
   #     evaluation_result_container = []
   #     evaluation_result_status = True
   #
   #     for expression in expressions:
   #         result = expression.evaluate_expression(sequence)
   #         evaluation_result_container.append(result.expression_status)
   #         if not result.satisfied:
   #             evaluation_result_status = False
   #             break
   #
   #     return evaluation_result_status, evaluation_result_container
   #
   #  TODO: Refactor
   # def to_dict(self):
   #     result = {
   #         'course_code': self.course_code.to_dict(),
   #         'name': self.name,
   #         'credits': self.credits,
   #         'hours_lectures': float(self.hours_lectures),
   #         'hours_labs': float(self.hours_labs),
   #         'hours_tutorials': float(self.hours_tutorials),
   #         'requirement': self.requirement
   #     }
   #     return result


class CourseOffering(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    term_type = models.PositiveSmallIntegerField(
        choices=[
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )

    def __str__(self):
        return str(self.course) + " - " + str(self.year) + " " + str(self.term_type)


class Section(models.Model):
    crn = models.IntegerField(primary_key=True)
    course_offering = models.ForeignKey(to=CourseOffering, on_delete=models.CASCADE)
    name = models.CharField(max_length=4)
    section_type = models.CharField(
        max_length=20,
        choices=[
            ('lecture', 'lecture'),
            ('lab', 'lab'),
            ('tutorial', 'tutorial')
        ]
    )

    def to_dict(self):
        result = {
            'crn': self.crn,
            'course_offering': self.course_offering.id,
            'name': self.name,
            'section_type': self.section_type
        }

        return result

    # TODO: Add location field

    # def does_section_conflict(self, section_to_compare):
    #     for meeting_to_compare in section_to_compare:
    #         for meeting in self.meetings:
    #             if meeting.does_meeting_conflict(meeting_to_compare):
    #                 return True
    #
    #     return False

    def __str__(self):
        return str(self.course_offering) + " - " + str(self.crn) + " - " + str(self.name)


class Meeting(models.Model):
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    # TODO: Ensure that when creating course, default value is False
    meet_M = models.BooleanField(blank=False, null=False, default=False)
    meet_T = models.BooleanField(blank=False, null=False, default=False)
    meet_W = models.BooleanField(blank=False, null=False, default=False)
    meet_R = models.BooleanField(blank=False, null=False, default=False)
    meet_F = models.BooleanField(blank=False, null=False, default=False)
    meet_S = models.BooleanField(blank=False, null=False, default=False)
    meet_Z = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        return str(self.section)

    def to_dict(self):
        result = {
            'section': self.section.crn,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'meet_M': self.meet_M,
            'meet_T': self.meet_T,
            'meet_W': self.meet_W,
            'meet_R': self.meet_R,
            'meet_F': self.meet_F,
            'meet_S': self.meet_S,
            'meet_Z': self.meet_Z
        }

        return result

    # def to_dict(self):
    #     result = {
    #         'days': [day.to_dict()['day'] for day in self.days],
    #         'location': self.location,
    #         'date_range': self.date_range,
    #         'time_range': self.time_range
    #     }
    #     return result


    #
    # def does_meeting_conflict(self, meeting_to_compare):
    #
    #     if not DateUtils.do_dates_overlap(self.date_range, meeting_to_compare.date_range):
    #         # Skip if the date ranges don't overlap
    #         return False
    #
    #     # If the start and end dates overlap for 6 days or less, then
    #     # we must only check the specific days they overlap for time
    #     # conflicts.
    #     if abs(meeting_to_compare.date_range.end_date - self.date_range.start_date) < datetime.timedelta(days=7) \
    #         or abs(self.date_range.end_date - meeting_to_compare.date_range.start_date) < datetime.timedelta(days=7):
    #
    #         overlapping_weekdays = DateUtils.get_weekdays_in_date_range(meeting_to_compare.date_range.start_date, self.date_range.end_date)
    #         # TODO: Double-check compatibility  with MeetingDay ArrayField
    #         weekdays_to_compare = [day for day in overlapping_weekdays if (day in meeting_to_compare.days) and (day in self.days)]
    #
    #         if len(weekdays_to_compare) == 0:
    #             return False
    #         if DateUtils.do_times_overlap(self.time_range, meeting_to_compare.time_range):
    #             return True
    #
    #     # Third case when overlap is 7 days or more. Any weekdays are applicable
    #     else:
    #         weekdays_to_compare = [day for day in list(Weekday) if (day in meeting_to_compare.days) and (day in self.days)]
    #         if len(weekdays_to_compare) == 0:
    #             return False
    #
    #         # TODO: Double-check compatibility with MeetingDay
    #         if DateUtils.do_times_overlap(self.time_range, meeting_to_compare.time_range):
    #             return True
    #
    #     return False
    #
