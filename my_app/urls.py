from django.urls import include, path
from . import views as my_app_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', my_app_view.homepage, name='home'),
    path('login/', my_app_view.loginpage, name='loginpage'),
    path('logout/', my_app_view.logoutpage, name='logout'),
    path('signup/', my_app_view.signup, name='signup'),
    path('contact/', my_app_view.contact, name='contact'),
    path('about-us/', my_app_view.about_us, name='about_us'),
    path('verification/', include('verify_email.urls')),
    path('subscribemonthly/', my_app_view.subscribe_monthly, name = 'paymonthly'),
    path('subscribequarterly/', my_app_view.subscribe_quarterly, name = 'payquarterly'),
    path('subscribemonthly/', my_app_view.subscribe_yearly, name = 'payyearly'),
    path('verify/', my_app_view.verify_payment, name = 'verify'),	
    path('dashboard/', my_app_view.dashboard, name = 'dashboard'),	
    path('corporate-plan/', my_app_view.corporate, name = 'corporate'),	
    path('verification-successful/', my_app_view.verification_successful, name = 'verified_page'),	
    path('verification-failed/', my_app_view.verification_failed, name = 'unverified_page'),	
    path('resend-email/', my_app_view.resend_email, name = 'resend_email'),	
    path('payment-successful/', my_app_view.payment_success, name = 'payment_success'),	
    path('corporate-successful/', my_app_view.corporate_sent, name = 'corporate_sent'),	
    path('search/', my_app_view.search_user, name = 'search'),	
    path('password-reset/', my_app_view.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='my_app/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='my_app/password_reset_complete.html'),
         name='password_reset_complete'),

]


