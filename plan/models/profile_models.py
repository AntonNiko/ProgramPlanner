from django.contrib.auth.models import User
from djongo import models
from .section_models import Schedule
from .sequence_models import Sequence

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sequence = models.EmbeddedField(
        model_container = Sequence
    )
    schedules = models.ArrayField(
        model_container = Schedule
    )
    # TODO: Add array of programs.