# core/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import Django's auth views for logout

urlpatterns = [
    path('', views.data_home, name='data_home'),
    path('summary/', views.summary_page, name='summary_page'), # KEEP THIS

    # Data listing URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('categories/', views.category_list, name='category_list'),
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('spend-entries/', views.spend_entry_list, name='spend_entry_list'),
    path('supplier-product-pricing/', views.supplier_product_pricing_list, name='supplier_product_pricing_list'),
    path('supplier-contracts/', views.supplier_contract_list, name='supplier_contract_list'),
    path('supplier-discounts/', views.supplier_discount_list, name='supplier_discount_list'),
    path('alternate-suppliers/', views.alternate_supplier_list, name='alternate_supplier_list'),

    # Export URLs
    path('export/<str:model_name>/', views.export_model_excel, name='export_model_excel'),

    # Edit and Delete URLs for each model
    path('edit/<str:model_name>/<int:pk>/', views.edit_model_record, name='edit_model_record'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_model_record, name='delete_model_record'),

    # Add a logout URL if you don't have one in your main urls.py
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]