# core/management/commands/load_brake_data.py
import csv
import os
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import (
    Supplier, Category, PurchaseOrder, Invoice, SpendEntry,
    SupplierProductPricing, SupplierContract, SupplierDiscount, AlternateSupplier
)


class Command(BaseCommand):
    help = "Load sample procurement data from CSV files for a brake manufacturing company."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Wiping existing data..."))

        # Delete in reverse order of dependencies to avoid FK issues
        AlternateSupplier.objects.all().delete()
        SupplierDiscount.objects.all().delete()
        SupplierContract.objects.all().delete()
        SupplierProductPricing.objects.all().delete()
        Invoice.objects.all().delete()
        SpendEntry.objects.all().delete() # SpendEntry does not have FKs to PO/Invoice, safe here
        PurchaseOrder.objects.all().delete()
        Category.objects.all().delete()
        Supplier.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Existing data wiped successfully."))

        # Define the path to your CSV data directory
        # Assuming CSVs are in core/data/
        data_dir = os.path.join(settings.BASE_DIR, 'core', 'data')

        # --- Load Suppliers ---
        self.stdout.write(self.style.SUCCESS("Loading Suppliers from supplier.csv..."))
        suppliers_by_id = {}
        try:
            with open(os.path.join(data_dir, 'supplier.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier = Supplier.objects.create(
                        id=int(row['id']), # Explicitly set ID if you want to match CSV IDs
                        name=row['name'],
                        contact_email=row['contact_email'],
                        phone=row['phone'] if row['phone'] else None,
                        address=row['address'] if row['address'] else None,
                        gstin=row['gstin'] if row['gstin'] else None,
                        pan=row['pan'] if row['pan'] else None,
                        score=float(row['score']),
                        type=row['type'],
                        is_active=(row['is_active'].lower() == 'true'),
                        share_of_business=Decimal(row['share_of_business']),
                        lead_time_days=int(row['lead_time_days']),
                        base_currency=row['base_currency'],
                        unit_of_measure=row['unit_of_measure']
                    )
                    suppliers_by_id[supplier.id] = supplier
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(suppliers_by_id)} suppliers."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: supplier.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading suppliers: {e}"))
            return

        # --- Load Categories ---
        self.stdout.write(self.style.SUCCESS("Loading Categories from category.csv..."))
        categories_by_id = {}
        # First pass for categories without parents
        try:
            with open(os.path.join(data_dir, 'category.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Store all category rows to process parents in a second pass
                category_rows = list(reader)
                
                for row in category_rows:
                    if not row['parent']: # Load categories that don't have a parent yet
                        category = Category.objects.create(
                            id=int(row['id']),
                            name=row['name'],
                            parent=None
                        )
                        categories_by_id[category.id] = category
            self.stdout.write(self.style.SUCCESS("Initial categories (without parents) loaded."))

            # Second pass to link parent categories
            for row in category_rows:
                if row['parent']:
                    parent_id = int(row['parent'])
                    if parent_id in categories_by_id:
                        parent_category = categories_by_id[parent_id]
                        # Check if category already exists (from first pass) or create it
                        if int(row['id']) not in categories_by_id:
                            category = Category.objects.create(
                                id=int(row['id']),
                                name=row['name'],
                                parent=parent_category
                            )
                            categories_by_id[category.id] = category
                        else: # If it already exists, just update its parent
                            category = categories_by_id[int(row['id'])]
                            category.parent = parent_category
                            category.save()
                    else:
                        self.stdout.write(self.style.WARNING(f"Parent category ID {parent_id} for category {row['name']} not found. Skipping parent link."))
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(categories_by_id)} categories."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: category.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading categories: {e}"))
            return


        # --- Load Purchase Orders ---
        self.stdout.write(self.style.SUCCESS("Loading Purchase Orders from purchaseorder.csv..."))
        purchase_orders_by_id = {}
        try:
            with open(os.path.join(data_dir, 'purchaseorder.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier_obj = suppliers_by_id.get(int(row['supplier']))
                    category_obj = categories_by_id.get(int(row['category'])) if row['category'] else None

                    if not supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping PO {row['po_number']}: Supplier ID {row['supplier']} not found."))
                        continue

                    po = PurchaseOrder.objects.create(
                        id=int(row['id']),
                        po_number=row['po_number'],
                        supplier=supplier_obj,
                        category=category_obj,
                        amount=Decimal(row['amount']),
                        issue_date=datetime.strptime(row['issue_date'], '%Y-%m-%d').date(),
                        status=row['status']
                    )
                    purchase_orders_by_id[po.id] = po
            self.stdout.write(self.style.SUCCESS(f"Loaded {len(purchase_orders_by_id)} purchase orders."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: purchaseorder.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading purchase orders: {e}"))
            return


        # --- Load Invoices ---
        self.stdout.write(self.style.SUCCESS("Loading Invoices from invoice.csv..."))
        try:
            with open(os.path.join(data_dir, 'invoice.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier_obj = suppliers_by_id.get(int(row['supplier']))
                    po_obj = purchase_orders_by_id.get(int(row['purchase_order'])) if row['purchase_order'] else None

                    if not supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping Invoice {row['invoice_number']}: Supplier ID {row['supplier']} not found."))
                        continue

                    paid_date = datetime.strptime(row['paid_date'], '%Y-%m-%d').date() if row['paid_date'] else None

                    Invoice.objects.create(
                        id=int(row['id']),
                        invoice_number=row['invoice_number'],
                        supplier=supplier_obj,
                        purchase_order=po_obj,
                        invoice_date=datetime.strptime(row['invoice_date'], '%Y-%m-%d').date(),
                        due_date=datetime.strptime(row['due_date'], '%Y-%m-%d').date(),
                        paid_date=paid_date,
                        amount=Decimal(row['amount']),
                        status=row['status']
                    )
            self.stdout.write(self.style.SUCCESS("Invoices loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: invoice.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading invoices: {e}"))
            return


        # --- Load Spend Entries ---
        self.stdout.write(self.style.SUCCESS("Loading Spend Entries from spendentry.csv..."))
        try:
            with open(os.path.join(data_dir, 'spendentry.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    category_obj = categories_by_id.get(int(row['category'])) if row['category'] else None
                    supplier_obj = suppliers_by_id.get(int(row['supplier'])) if row['supplier'] else None

                    SpendEntry.objects.create(
                        id=int(row['id']),
                        category=category_obj,
                        supplier=supplier_obj,
                        date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                        amount=Decimal(row['amount']),
                        cost_center=row['cost_center'],
                        description=row['description'] if row['description'] else None
                    )
            self.stdout.write(self.style.SUCCESS("Spend entries loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: spendentry.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading spend entries: {e}"))
            return


        # --- Load Supplier Product Pricing ---
        self.stdout.write(self.style.SUCCESS("Loading Supplier Product Pricing from supplierproductpricing.csv..."))
        try:
            with open(os.path.join(data_dir, 'supplierproductpricing.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier_obj = suppliers_by_id.get(int(row['supplier']))

                    if not supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping Product Pricing for {row['product_name']}: Supplier ID {row['supplier']} not found."))
                        continue

                    SupplierProductPricing.objects.create(
                        id=int(row['id']),
                        supplier=supplier_obj,
                        product_name=row['product_name'],
                        price=Decimal(row['price']),
                        currency=row['currency'],
                        unit_of_measure=row['unit_of_measure']
                    )
            self.stdout.write(self.style.SUCCESS("Supplier product pricing loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: supplierproductpricing.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading supplier product pricing: {e}"))
            return


        # --- Load Supplier Contracts ---
        self.stdout.write(self.style.SUCCESS("Loading Supplier Contracts from suppliercontract.csv..."))
        try:
            with open(os.path.join(data_dir, 'suppliercontract.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier_obj = suppliers_by_id.get(int(row['supplier']))

                    if not supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping Contract {row['contract_name']}: Supplier ID {row['supplier']} not found."))
                        continue

                    SupplierContract.objects.create(
                        id=int(row['id']),
                        supplier=supplier_obj,
                        contract_name=row['contract_name'],
                        start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date(),
                        end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date(),
                        terms=row['terms']
                    )
            self.stdout.write(self.style.SUCCESS("Supplier contracts loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: suppliercontract.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading supplier contracts: {e}"))
            return


        # --- Load Supplier Discounts ---
        self.stdout.write(self.style.SUCCESS("Loading Supplier Discounts from supplierdiscount.csv..."))
        try:
            with open(os.path.join(data_dir, 'supplierdiscount.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    supplier_obj = suppliers_by_id.get(int(row['supplier']))

                    if not supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping Discount for {row['product_name']}: Supplier ID {row['supplier']} not found."))
                        continue

                    SupplierDiscount.objects.create(
                        id=int(row['id']),
                        supplier=supplier_obj,
                        product_name=row['product_name'],
                        discount_percent=Decimal(row['discount_percent']),
                        valid_from=datetime.strptime(row['valid_from'], '%Y-%m-%d').date(),
                        valid_to=datetime.strptime(row['valid_to'], '%Y-%m-%d').date()
                    )
            self.stdout.write(self.style.SUCCESS("Supplier discounts loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: supplierdiscount.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading supplier discounts: {e}"))
            return


        # --- Load Alternate Suppliers ---
        self.stdout.write(self.style.SUCCESS("Loading Alternate Suppliers from alternatesupplier.csv..."))
        try:
            with open(os.path.join(data_dir, 'alternatesupplier.csv'), 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    primary_supplier_obj = suppliers_by_id.get(int(row['primary_supplier']))
                    alternate_supplier_obj = None
                    if row['alternate_supplier']: # Check if alternate_supplier exists in CSV
                        alternate_supplier_obj = suppliers_by_id.get(int(row['alternate_supplier']))

                    if not primary_supplier_obj:
                        self.stdout.write(self.style.ERROR(f"Skipping Alternate Supplier for {row['product_name']}: Primary Supplier ID {row['primary_supplier']} not found."))
                        continue

                    AlternateSupplier.objects.create(
                        id=int(row['id']),
                        product_name=row['product_name'],
                        primary_supplier=primary_supplier_obj,
                        alternate_supplier=alternate_supplier_obj, # This can be None
                        lead_time_days=int(row['lead_time_days'])
                    )
            self.stdout.write(self.style.SUCCESS("Alternate suppliers loaded successfully."))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: alternatesupplier.csv not found at {data_dir}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading alternate suppliers: {e}"))
            return


        self.stdout.write(self.style.SUCCESS("✅ All sample brake manufacturing data loaded successfully from CSVs!"))