from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_future(value):
    if (value > timezone.now()):
        raise ValidationError('Cannot assign or receive in the future!')