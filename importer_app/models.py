import os

from django.db import models


class ProductFile(models.Model):

    file = models.FileField(max_length=50)
    created_date = models.DateTimeField(auto_now=True)

    def filename(self):
        return os.path.basename(self.file.name)


class ProductInfo(models.Model):

    ACTIVE = 1
    INACTIVE = 2

    PRODUCT_STATUS = ((ACTIVE, "Active"), (INACTIVE, "Inactive"))

    name = models.CharField(max_length=240)
    sku = models.CharField(max_length=240, unique=True, db_index=True)
    description = models.TextField(null=True)
    status = models.SmallIntegerField(choices=PRODUCT_STATUS, default=ACTIVE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


class ProductWebHook(models.Model):

    name = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
