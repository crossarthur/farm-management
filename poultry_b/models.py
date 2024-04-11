from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.


class ChickenFigures_b(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    customer_rank = models.CharField(max_length=100, null=True, blank=True,)
    customer = models.CharField(max_length=100, null=True, blank=True,)
    chicken_in = models.IntegerField(default=0, null=True, blank=True)
    chicken_out = models.IntegerField(default=0, null=True, blank=True)
    chicken_mortality = models.IntegerField(default=0, null=True, blank=True)
    chicken_slaughtered = models.IntegerField(default=0, null=True, blank=True)
    chicken_out_kilogram = models.DecimalField(default=0.0, decimal_places=2, max_digits=6, null=True, blank=True)
    chicken_out_unit_price = models.IntegerField(default=0, null=True, blank=True)
    chicken_out_total_cost = models.IntegerField(default=0, null=True, blank=True)
    total_chicken = models.IntegerField(null=True, blank=True, default=0)
    date = models.DateTimeField(auto_now_add=True)


class CustomerRank_b(models.Model):
    customer_rk = models.CharField(max_length=100, null=True, blank=True)


class Feed_b(models.Model):
    feed_description = models.CharField(max_length=100)
    feed_quantity = models.IntegerField(null=True, blank=True)
    feed_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.feed_description


class Drugs_b(models.Model):
    drug_description = models.CharField(max_length=100)
    drug_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.drug_description


class Necessities_b(models.Model):
    necessities_description = models.CharField(max_length=100)
    necessities_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.necessities_description


class ColdRoomIn_b(models.Model):
    chickens_in_freezer = models.IntegerField(default=1, null=True, blank=True)
    total_coldroom = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)


class ColdRoomOut(models.Model):
    chickens_out_freezer = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)


class Production_b(models.Model):
    production_description = models.CharField(max_length=100)
    production_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return self.production_description


class Imprest_b(models.Model):
    total_imprest = models.IntegerField(default=0, null=True, blank=True)
    imprest = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class NotePad_b(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    note = RichTextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class Offals_b(models.Model):
    offals_description = models.CharField(max_length=100)
    offals_cost = models.IntegerField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=False)


class Profit_b(models.Model):
    income = models.IntegerField(null=True, blank=True)
    expenditure = models.IntegerField(null=True, blank=True)
    calculate = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
