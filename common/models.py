from django.db import models
from uuid import uuid4
from django_countries.fields import CountryField
from .constants import *


# Create your models here.
class CommonModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Address(models.Model):
    unit_no = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=True, null=False
    )
    street_no = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=True, null=False
    )
    line_1 = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=True, null=False
    )
    line_2 = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=True, null=False
    )
    city = models.Charfield(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=False, null=False
    )
    region = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=False, null=False
    )
    postal_code = models.CharField(
        max_length=MODEL_CHARFIELD_MAX_LENGTH, blank=False, null=False
    )
    country = CountryField(blank=False, null=False)


class ModelHasAddress(models.Model):
    address = models.ForeignKey(to=Address, on_delete=models.PROTECT)


