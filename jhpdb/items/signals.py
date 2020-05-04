from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from django.utils import timezone
from .models import Item, ItemAssign


@receiver(pre_save, sender=ItemAssign)
def assign_by_IT(sender, instance, **kwargs):
    if((instance.received_by) and (instance.received_by.department.department!='IT')):
        raise Exception("Only members of IT Staff can receive items")
    elif((instance.assign_by) and (instance.assign_by.department.department!='IT')):
        raise Exception("Only members of IT Staff can assign items")

@receiver(post_save, sender=ItemAssign)
def item_status_check_after_assign(sender, instance, created, **kwargs):
    if ((created) and (not instance.received_date) and (instance.assign_status=='0')):
        Item.objects.filter(pk=instance.item.pk).update(status='Assigned to '+instance.assign_to.user.username)
    elif ((not created) and (instance.received_date) and (instance.assign_status=='1')):
        Item.objects.filter(pk=instance.item.pk).update(status='In stock')
    elif ((not created) and (instance.received_date) and (instance.assign_status=='2')):
        Item.objects.filter(pk=instance.item.pk).update(status='Expended by '+instance.assign_to.user.username)
    elif ((not created) and (instance.received_date) and (instance.assign_status=='3')):
        Item.objects.filter(pk=instance.item.pk).update(status='Lost by '+instance.assign_to.user.username)
    elif ((not created) and (instance.received_date) and (instance.assign_status=='4')):
        Item.objects.filter(pk=instance.item.pk).update(status='Damaged by '+instance.assign_to.user.username)
    else:
        raise Exception('Invalid Entry! (from items.signals.item_status_check_after_assign)')

@receiver(pre_delete, sender=ItemAssign)
def received_check_before_delete(sender, instance, **kwargs):
    if ((instance.assign_status=='0')):
        raise Exception('Cannot be deleted till it is assigned')
