# core/views.py
import csv
import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import date
from decimal import Decimal
import datetime # Import datetime module for handling dates/datetimes

# Import openpyxl for Excel export
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from .models import (
    Supplier, Category, PurchaseOrder, Invoice, SpendEntry,
    SupplierProductPricing, SupplierContract, SupplierDiscount, AlternateSupplier
)
from django.db.models import ForeignKey, OneToOneField # Import these for field type checking

@login_required
def data_home(request):
    """Renders the main Data page with links to sub-pages."""
    return render(request, 'core/data_home.html')

@login_required
def summary_page(request):
    """Renders the Summary page (placeholder for now)."""
    return render(request, 'core/summary_page.html')

# Generic function to fetch and render model lists
def _render_model_list(request, model, title, fields_to_display):
    """Helper function to fetch all objects of a model and render them."""
    objects = model.objects.all().values() # Get all fields as dictionary
    
    # Convert Decimal and related objects for JSON serialization
    data_list = []
    for obj in objects:
        cleaned_obj = {}
        for key, value in obj.items():
            if isinstance(value, float):
                cleaned_obj[key] = round(value, 2) # Format floats
            elif isinstance(value, (int, float, complex)) and not isinstance(value, bool):
                 cleaned_obj[key] = int(value) if value == int(value) else value # Show integers as integers
            elif isinstance(value, Decimal):
                cleaned_obj[key] = str(value) # Convert Decimal to string
            elif isinstance(value, date): # Handle date objects
                cleaned_obj[key] = value.isoformat() # Convert date to ISO format string
            elif isinstance(value, datetime.datetime): # Handle datetime objects
                cleaned_obj[key] = value.isoformat()
            # Handle ForeignKey fields to show related object's __str__
            # This requires fetching the actual object, which can be inefficient
            # For DataTables, it's often better to pre-fetch or handle in template JS
            # For now, we'll try to get the __str__ or ID
            elif hasattr(model._meta.get_field(key), 'related_model'):
                try:
                    # Get the actual model instance to access the ForeignKey relationship
                    instance = model.objects.get(pk=obj['id'])
                    fk_value = getattr(instance, key)
                    if fk_value:
                        cleaned_obj[key] = str(fk_value) # Use __str__ representation
                    else:
                        cleaned_obj[key] = 'N/A'
                except model.DoesNotExist:
                    cleaned_obj[key] = 'N/A' # Object not found (shouldn't happen with .all())
                except Exception:
                    cleaned_obj[key] = value # Fallback if FK resolution fails or it's a value directly
            else:
                cleaned_obj[key] = value
        data_list.append(cleaned_obj)

    context = {
        'title': title,
        'data': data_list,
        'fields': fields_to_display, # Fields for table headers
    }
    return render(request, 'core/model_list.html', context)

# --- NEW EXCEL EXPORT VIEW ---
@login_required
def export_model_excel(request, model_name):
    # Mapping for slugified model names to actual Django model classes
    model_map = {
        'supplier-data': Supplier, # Corresponds to title|slugify for Supplier Data
        'category-data': Category,
        'purchase-order-data': PurchaseOrder,
        'invoice-data': Invoice,
        'spend-entry-data': SpendEntry,
        'supplier-product-pricing-data': SupplierProductPricing,
        'supplier-contract-data': SupplierContract,
        'supplier-discount-data': SupplierDiscount,
        'alternate-supplier-data': AlternateSupplier,
    }
    
    model = model_map.get(model_name)
    if not model:
        return HttpResponse("Model not found.", status=404)

    # Determine fields to export (using actual model fields for better accuracy)
    fields_to_export = []
    for field in model._meta.get_fields(include_hidden=False):
        # Exclude auto-generated reverse relations (e.g., related_name for FKs)
        # Exclude ManyToMany fields for simplicity in direct Excel export
        if field.concrete and not field.auto_created and not field.many_to_many:
            fields_to_export.append(field) # Append field object, not just name

    # Create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = model.__name__ + " Data"

    # Define a simple style for headers
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = openpyxl.styles.PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    border_thin = Side(style='thin', color="000000")
    header_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
    
    # Write headers
    headers = []
    for field in fields_to_export:
        headers.append(field.verbose_name.replace('_', ' ').title()) # Use verbose_name for friendly headers

    worksheet.append(headers)
    for cell in worksheet[1]: # Apply style to header row
        cell.font = header_font
        cell.fill = header_fill
        cell.border = header_border
        cell.alignment = Alignment(horizontal="center", vertical="center")


    # Write data rows
    for obj in model.objects.all():
        row_data = []
        for field in fields_to_export:
            value = getattr(obj, field.name)
            
            if isinstance(field, (ForeignKey, OneToOneField)):
                # For ForeignKey/OneToOne, use the string representation
                row_data.append(str(value) if value else 'N/A')
            elif isinstance(value, (date, datetime.date, datetime.datetime)): # Handle dates/datetimes
                row_data.append(value) # openpyxl handles date/datetime objects directly
            elif isinstance(value, Decimal):
                row_data.append(float(value)) # Convert Decimal to float for Excel
            elif isinstance(value, bool):
                row_data.append("Yes" if value else "No") # Represent booleans as Yes/No
            else:
                row_data.append(value)
        worksheet.append(row_data)

    # Adjust column widths
    for col_idx, col in enumerate(worksheet.columns, 1):
        max_length = 0
        column = get_column_letter(col_idx) # Get the column name (A, B, C, ...)
        for cell in col:
            try:
                # Convert value to string and check length. Handle None gracefully.
                cell_value_str = str(cell.value) if cell.value is not None else ""
                if len(cell_value_str) > max_length:
                    max_length = len(cell_value_str)
            except:
                pass # Ignore errors for complex cell types if any
        adjusted_width = (max_length + 2) # Add some padding
        if adjusted_width > 75: # Cap max width to prevent excessively wide columns
            adjusted_width = 75
        elif adjusted_width < 10: # Ensure minimum width
            adjusted_width = 10
        worksheet.column_dimensions[column].width = adjusted_width

    # Create the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{model.__name__.lower()}_data.xlsx"'
    workbook.save(response)
    return response

# Specific views for each model (remain mostly unchanged, but ensure 'fields' match your needs)
@login_required
def supplier_list(request):
    fields = ['id', 'name', 'contact_email', 'phone', 'address', 'gstin', 'pan', 'score', 'type', 'is_active', 'share_of_business', 'lead_time_days', 'base_currency', 'unit_of_measure']
    return _render_model_list(request, Supplier, 'Supplier Data', fields)

@login_required
def category_list(request):
    fields = ['id', 'name', 'parent'] # 'parent' will show ID, can enhance to name if needed
    return _render_model_list(request, Category, 'Category Data', fields)

@login_required
def purchase_order_list(request):
    fields = ['id', 'po_number', 'supplier', 'category', 'amount', 'issue_date', 'status']
    return _render_model_list(request, PurchaseOrder, 'Purchase Order Data', fields)

@login_required
def invoice_list(request):
    fields = ['id', 'invoice_number', 'supplier', 'purchase_order', 'invoice_date', 'due_date', 'paid_date', 'amount', 'status']
    return _render_model_list(request, Invoice, 'Invoice Data', fields)

@login_required
def spend_entry_list(request):
    fields = ['id', 'category', 'supplier', 'date', 'amount', 'cost_center', 'description']
    return _render_model_list(request, SpendEntry, 'Spend Entry Data', fields)

@login_required
def supplier_product_pricing_list(request):
    fields = ['id', 'supplier', 'product_name', 'price', 'currency', 'unit_of_measure']
    return _render_model_list(request, SupplierProductPricing, 'Supplier Product Pricing Data', fields)

@login_required
def supplier_contract_list(request):
    fields = ['id', 'supplier', 'contract_name', 'start_date', 'end_date', 'terms']
    return _render_model_list(request, SupplierContract, 'Supplier Contract Data', fields)

@login_required
def supplier_discount_list(request):
    fields = ['id', 'supplier', 'product_name', 'discount_percent', 'valid_from', 'valid_to']
    return _render_model_list(request, SupplierDiscount, 'Supplier Discount Data', fields)

@login_required
def alternate_supplier_list(request):
    fields = ['id', 'product_name', 'primary_supplier', 'alternate_supplier', 'lead_time_days']
    return _render_model_list(request, AlternateSupplier, 'Alternate Supplier Data', fields)