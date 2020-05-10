from django.contrib.auth.models import User
from djongo import models
from .program_models import Program
from .section_models import Schedule
from .sequence_models import Sequence


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_sequence = models.EmbeddedField(
        model_container=Sequence,
        blank=True
    )
    # saved_sequences to be implemented later, only use active_sequence atm.
    saved_sequences = models.ArrayField(
        model_container=Sequence
    )
    active_schedule = models.EmbeddedField(
        model_container=Schedule,
        blank=True
    )
    saved_schedules = models.ArrayField(
        model_container=Schedule
    )
    programs = models.ArrayField(
        model_container=Program
    )
