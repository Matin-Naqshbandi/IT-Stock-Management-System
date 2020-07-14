from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Employee
from allauth.account.models  import EmailAddress
from django.core.exceptions import ValidationError

# login error happens
# @receiver(pre_save, sender=User)
# def add_email_address(sender, instance, **kwargs):
#     User.objects.filter(pk=instance.user.pk).update(email=instance.username+'@jhpiego.org')

@receiver(post_save, sender=User)
def create_user_employee(sender, instance, created, **kwargs):
    if created:
        Employee.objects.create(user=instance)
        EmailAddress.objects.create(user=instance, email=instance.username+'@jhpiego.org', verified=True, primary=True)

@receiver(post_save, sender=User)
def save_user_employee(sender, created, instance, **kwargs):
    instance.employee.save()
    if(not created and instance.username):
        EmailAddress.objects.filter(pk=instance.pk).update(email=instance.username+'@jhpiego.org')