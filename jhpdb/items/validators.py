from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator

def validate_future(value):
    if (value > timezone.now()):
        raise ValidationError('Cannot assign or receive in the future!')
