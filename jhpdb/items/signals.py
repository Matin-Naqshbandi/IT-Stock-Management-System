from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.utils import timezone
from .models import Item, ItemAssign, Model
from django.db.models import F
from django.core.exceptions import ValidationError

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
        raise ValidationError('Invalid Entry! (from items.signals.item_status_check_after_assign)')

@receiver(pre_delete, sender=ItemAssign)
def received_check_before_delete(sender, instance, **kwargs):
    if ((instance.assign_status=='0')):
        raise Exception('Cannot be deleted till it is assigned')

@receiver(pre_save, sender=ItemAssign)
def serial_and_tag_check_before_assigning_unexpendables(sender, instance, **kwargs):
    if(not(instance.item.serial and instance.item.tag_no)):
        raise ValidationError('Cannot assign unexpendable items without Serial and Tag_no!')

@receiver(pre_save, sender=Item)
def no_tag_no_for_expendables(sender, instance, **kwargs):
    if(instance.tag_no and instance.model.expendable):
        raise ValidationError('Cannot give Expendable items Tag_no!')

@receiver(post_delete, sender=Item)
def decrease_model_item_count_after_delete(sender, instance, **kwargs):
    Model.objects.filter(name=instance.model).update(item_count=F('item_count')-1)

@receiver(pre_save, sender=Model)
def check_item_count_before_save(sender, instance, **kwargs):
    if((not instance.pk) and (0<instance.item_count<=50)):
        pass
    elif((not instance.pk) and not(0<instance.item_count<=50)):
        raise ValidationError('Cannot enter item count lesser than 1 and more than 50!')
    elif((instance.pk) and (Item.objects.filter(model=instance.pk).count() > instance.item_count)):
        raise ValidationError('Cannot decreese item count, you need to delete item from Item model!')
    elif((instance.pk) and not((instance.item_count - Item.objects.filter(model=instance.pk).count())>50)):
        pass
    elif((instance.pk) and ((instance.item_count - Item.objects.filter(model=instance.pk).count())>50)):
        raise Exception('Can only enter batch of up to 50 items at a time!')
    else:
        raise ValidationError('Invalid Entry! (from items.signals.check_item_count_before_save)')
        
@receiver(post_save, sender=Model)
def Create_Model_Items(sender, instance, created, **kwargs):
    if((created) and (0<instance.item_count<=50)):
        for i in range(instance.item_count):
            Item.objects.create(manufacturer=instance.manufacturer, category=instance.category, model=instance)
    elif((not created) and (0<=(instance.item_count - Item.objects.filter(model=instance.pk).count())<=50)):
        for i in range(instance.item_count - Item.objects.filter(model=instance.pk).count()):
            Item.objects.create(manufacturer=instance.manufacturer, category=instance.category, model=instance)
    else:
        raise ValidationError('Invalid Entry! (from items.signals.Create_Model_Items)')