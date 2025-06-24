# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # New URL for Excel export - make sure it's before specific data paths to avoid conflicts
    path('export/excel/<str:model_name>/', views.export_model_excel, name='export_model_excel'),

    # Main data and summary pages
    path('data/', views.data_home, name='data_home'),
    path('summary/', views.summary_page, name='summary_page'),

    # Sub-pages for each loaded data type
    path('data/suppliers/', views.supplier_list, name='supplier_list'),
    path('data/categories/', views.category_list, name='category_list'),
    path('data/purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('data/invoices/', views.invoice_list, name='invoice_list'),
    path('data/spend-entries/', views.spend_entry_list, name='spend_entry_list'),
    path('data/product-pricing/', views.supplier_product_pricing_list, name='supplier_product_pricing_list'),
    path('data/contracts/', views.supplier_contract_list, name='supplier_contract_list'),
    path('data/discounts/', views.supplier_discount_list, name='supplier_discount_list'),
    path('data/alternate-suppliers/', views.alternate_supplier_list, name='alternate_supplier_list'),

    # Redirects the root URL to the data home page after login
    path('', views.data_home, name='home'),
]