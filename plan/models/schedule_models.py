#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

import datetime
from django.contrib.auth.models import User
from django.db import models
from plan.utils import DateUtils, Weekday
from .course_models import Section


class Schedule(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()
    term = models.PositiveSmallIntegerField(
        choices=[
            (1, 'spring'),
            (2, 'summer'),
            (3, 'fall')
        ]
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user) + " - " + self.name

    # def does_section_conflict(self, section_to_compare):
    #     result = {'conflicts': False, 'data': []}
    #     for section in self.sections.all():
    #         conflict_exists = section.does_section_conflict(section_to_compare)
    #         if conflict_exists:
    #             result['conflicts'] = True
    #             result['data'].append(section.crn)
    #
    #     return result
    #
    # def to_dict(self):
    #     result = {
    #         'year': self.year,
    #         'term_type': self.term_type,
    #         'name': self.name,
    #         'sections': [section.to_dict() for section in self.sections.all()]
    #     }
    #     return result


class ScheduleSection(models.Model):
    schedule = models.ForeignKey(to=Schedule, on_delete=models.CASCADE)
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.schedule) + " - " + str(self.section)