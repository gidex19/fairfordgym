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
    path('corporate-plan/', my_app_view.corporate, name = 'corporate'),	
    path('verification-successful/', my_app_view.verification_successful, name = 'verified_page'),	
    path('verification-failed/', my_app_view.verification_failed, name = 'unverified_page'),	
    path('resend-email/', my_app_view.resend_email, name = 'resend_email'),	
    path('payment-successful/', my_app_view.payment_success, name = 'payment_success'),	
    path('corporate-successful/', my_app_view.corporate_sent, name = 'corporate_sent'),	
    path('search/', my_app_view.search_user, name = 'search'),	

]