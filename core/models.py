# core/models.py
from django.db import models

class Supplier(models.Model):
    # AutoField 'id' is implicit as Django's primary key by default
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField(default=0.0)
    type = models.CharField(max_length=20)  # Direct or Indirect
    is_active = models.BooleanField(default=True)
    share_of_business = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    lead_time_days = models.IntegerField(default=0)
    base_currency = models.CharField(max_length=10, default='INR')
    unit_of_measure = models.CharField(max_length=20, default='Unit')

    def __str__(self):
        return self.name


class Category(models.Model):
    # AutoField 'id' is implicit
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    # AutoField 'id' is implicit
    po_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.po_number


class Invoice(models.Model):
    # AutoField 'id' is implicit
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.invoice_number


class SpendEntry(models.Model):
    # AutoField 'id' is implicit
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    cost_center = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        # Added __str__ for SpendEntry for better admin readability
        return f"Spend on {self.category.name if self.category else 'N/A'} by {self.supplier.name if self.supplier else 'N/A'} on {self.date}"


class SupplierProductPricing(models.Model):
    # AutoField 'id' is implicit
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10)
    unit_of_measure = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product_name} - {self.supplier.name} ({self.price} {self.currency})"


class SupplierContract(models.Model):
    # AutoField 'id' is implicit
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    contract_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    terms = models.TextField()

    def __str__(self):
        return f"{self.contract_name} ({self.supplier.name})"


class SupplierDiscount(models.Model):
    # AutoField 'id' is implicit
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateField()
    valid_to = models.DateField()

    def __str__(self):
        return f"Discount for {self.product_name} by {self.supplier.name} ({self.discount_percent}%)"


class AlternateSupplier(models.Model):
    # AutoField 'id' is implicit
    product_name = models.CharField(max_length=255)
    primary_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='primary_for')
    alternate_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='alternate_for', null=True, blank=True) # Added null/blank for cases where alt_supplier might be missing
    lead_time_days = models.IntegerField()

    def __str__(self):
        return f"Alt Supplier for {self.product_name}: {self.alternate_supplier.name if self.alternate_supplier else 'N/A'}"