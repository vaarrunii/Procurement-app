from django.db import models

# Supplier Table
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


# Category Table
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


# Purchase Order Table
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('Issued', 'Issued'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ])

    def __str__(self):
        return self.po_number


# Invoice Table
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue')
    ])

    def __str__(self):
        return self.invoice_number


# Spend Entry Table
class SpendEntry(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    cost_center = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - ₹{self.amount} - {self.supplier.name}"
