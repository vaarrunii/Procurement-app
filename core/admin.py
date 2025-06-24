from django.contrib import admin
from .models import (
    Supplier,
    SupplierContract,
    SupplierDiscount,
    SupplierProductPricing,
    Category,
    PurchaseOrder,
    Invoice,
)

admin.site.register(Supplier)
admin.site.register(SupplierContract)
admin.site.register(SupplierDiscount)
admin.site.register(SupplierProductPricing)
admin.site.register(Category)
admin.site.register(PurchaseOrder)
admin.site.register(Invoice)
