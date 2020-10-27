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
    term = models.CharField(
        choices=[
            ('spring', 'spring'),
            ('summer', 'summer'),
            ('fall', 'fall')
        ],
        max_length=10
    )
    name = models.CharField(max_length=100)

    def to_dict(self):
        result = {
            'id': self.id,
            'year': self.year,
            'term': self.term,
            'name': self.name,
        }
        return result

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


class ScheduleSection(models.Model):
    schedule = models.ForeignKey(to=Schedule, on_delete=models.CASCADE)
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.schedule) + " - " + str(self.section)