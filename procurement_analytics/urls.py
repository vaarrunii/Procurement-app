# procurement_analytics_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Import Django's built-in auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    # Add this line to map the login page directly to /login/
    # IMPORTANT: Specify your custom template_name here!
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    # Also, it's good practice to specify where to go after logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    path('', include('core.urls')), # Include URLs from your core app
]