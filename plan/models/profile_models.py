from django.contrib.auth.models import User
from djongo import models
from .program_models import Program
from .schedule_models import Schedule
from .sequence_models import Sequence


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active_sequence = models.EmbeddedField(
        model_container=Sequence,
        blank=True
    )
    # saved_sequences to be used later
    saved_sequences = models.ArrayReferenceField(
        to=Sequence,
        on_delete=models.CASCADE
    )
    # active_schedule to be used later
    active_schedule = models.EmbeddedField(
        model_container=Schedule,
        blank=True
    )
    saved_schedules = models.ArrayReferenceField(
        to=Schedule,
        on_delete=models.CASCADE
    )
    programs = models.ArrayReferenceField(
        to=Program,
        on_delete=models.CASCADE
    )
    # TODO: Add user preferences for sequence and schedule coordination
