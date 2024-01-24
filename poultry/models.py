from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.


class ChickenDetails(models.Model):
    total_chicken = models.IntegerField(null=True, blank=True)


class ChickenFigures(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    customer_rank = models.CharField(max_length=100, null=True, blank=True,)
    customer = models.CharField(max_length=100, null=True, blank=True,)
    chicken_in = models.IntegerField(default=0, null=True, blank=True)
    chicken_out = models.IntegerField(default=0, null=True, blank=True)
    chicken_mortality = models.IntegerField(default=0, null=True, blank=True)
    chicken_slaughtered = models.IntegerField(default=0, null=True, blank=True)
    chicken_out_kilogram = models.DecimalField(default=0.0, decimal_places=2, max_digits=5, null=True, blank=True)
    chicken_out_unit_price = models.IntegerField(default=0, null=True, blank=True)
    chicken_out_total_cost = models.IntegerField(default=0, null=True, blank=True)
    total_chicken = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)




'''def save(self, *args, **kwargs):
        # Set both fields to the same value before saving
        if self.customer is None:
            self.customer = self.customer_rank  # Set field1 to field2's value
        super(ChickenFigures, self).save(*args, **kwargs)  # Call the original save method'''

class CustomerRank(models.Model):
    customer_rk = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.customer_rk

'''@receiver(pre_save, sender=ChickenFigures)
def set_balance(sender, instance, *args, **kwargs):

    if instance.chicken_out is not None:
        instance.chicken_out_total_cost = instance.chicken_out_kilogram * instance.chicken_out_unit_price * instance.chicken_out
    else:
        pass'''


class Feed(models.Model):
    feed_description = models.CharField(max_length=100)
    feed_quantity = models.IntegerField(null=True, blank=True)
    feed_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.feed_description


class Drugs(models.Model):
    drug_description = models.CharField(max_length=100)
    drug_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.drug_description


class Necessities(models.Model):
    necessities_description = models.CharField(max_length=100)
    necessities_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.necessities_description


class ColdRoomIn(models.Model):
    chickens_in_freezer = models.IntegerField(default=1, null=True, blank=True)
    total_coldroom = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)


class ColdRoomOut(models.Model):
    chickens_out_freezer = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)


class Production(models.Model):
    production_description = models.CharField(max_length=100)
    production_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.production_description


class Profit(models.Model):
    income = models.IntegerField(null=True, blank=True)
    expenditure = models.IntegerField(null=True, blank=True)
    calculate = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Imprest(models.Model):
    total_imprest = models.IntegerField(default=0, null=True, blank=True)
    imprest = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class NotePad(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Offals(models.Model):
    offals_description = models.CharField(max_length=100)
    offals_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)
