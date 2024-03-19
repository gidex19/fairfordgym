from django.urls import include, path
from . import views as my_app_view

urlpatterns = [
    path('', my_app_view.homepage, name='home'),
    path('login/', my_app_view.loginpage, name='loginpage'),
    path('logout/', my_app_view.logoutpage, name='logout'),
    path('signup/', my_app_view.signup, name='signup'),
    path('contact/', my_app_view.contact, name='contact'),
    path('verification/', include('verify_email.urls')),
    path('subscribemonthly/', my_app_view.subscribe_monthly, name = 'paymonthly'),
    path('verify/', my_app_view.verify_payment, name = 'verify'),	
    path('dashboard/', my_app_view.dashboard, name = 'dashboard'),	
]