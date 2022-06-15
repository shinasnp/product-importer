from django.contrib import admin

# Register your models here.
from .models import ProductFile, ProductInfo, ProductWebHook

admin.site.register(ProductFile)
admin.site.register(ProductInfo)
admin.site.register(ProductWebHook)
