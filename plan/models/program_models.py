#  Copyright (c) 2020. by Anton Nikitenko
#  All rights reserved.

from django.db import models


class Program(models.Model):
    name = models.CharField(max_length=50)

    #TODO: Refactor
    def to_dict(self):
        result = {
            'institution': self.institution,
            'name': self.name,
            'requirements': self.requirements
        }
        return result
