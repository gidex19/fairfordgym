from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm, CorporateForm, ResendEmailForm, SearchUserForm
from .models import MyCustomuser as Customuser, Payment, CorporateMemberRequest
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from verify_email.email_handler import send_verification_email
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

# paystack_secret_key = "sk_test_9b5f4ffd691edd7e62673ce7e3bba49b123c98d6"
# paystack_public_key = "pk_test_e20dc9cbbd4bc7ac08b1ce0940c34f7714e5ab91" 
# paystack_secret_key = "sk_test_e56f0936942534b4bb68c97f96ec5478d3177c2d"
# paystack_public_key = "pk_test_b5844de2f9b615efc128374d8b500c7109d903bd" 
paystack_secret_key = "sk_test_3d0074c520b6c9d592d10d5ff4b820887ecb3acd"
paystack_public_key = "pk_test_6d42b1c09dc2b89577d36411df441587a7fe7a6e" 
paystack = Paystack(secret_key=paystack_secret_key)

def homepage(request):
    if request.method =='POST':
        contact_form = ContactForm(request.POST)
    else:
        contact_form = ContactForm()
    return render(request, 'my_app/home.html', {'contact_form': contact_form})

def loginpage(request):
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email_address')
            password = login_form.cleaned_data.get('password')
            email = email.lower()
            if Customuser.objects.filter(email=email).exists():
                custom_user = authenticate(
                    request, username=email, password=password)
                print(custom_user)
                if custom_user is not None:
                    # messages.success(request, 'Login Succesful')
                    login(request, custom_user)
                    print(
                        "Hello custom_user.full_name, You have been logged in successfully...")
                    messages.success(
                        request, 'Login successful')
                    #print('user has been logged in')

                    return redirect('home')
                elif custom_user is None:
                    print('message section')
                    messages.warning(
                        request, 'Incorrect email address or ppassword')
            else:
                messages.warning(
                    request, 'Email address not recognised')
                return redirect('login')
    else:
        login_form = LoginForm()
    return render(request, 'my_app/login.html', {'login_form': login_form})

def logoutpage(request):
    logout(request)
    messages.warning(request, 'Logout successfully')
    return redirect('loginpage')


@login_required
def search_user(request):
    if request.method =='POST':
        form  = ResendEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email').lower()
            if Customuser.objects.filter(email=email).exists():
                user = Customuser.objects.filter(email=email).first()
                print("user is present in the database")
                print(user.full_name)
            else:
                print("user is absent")
                user = 'None'
        else:
            print("search form invalid")        
    else:
        form = ResendEmailForm()  
    return render(request, 'my_app/search_user.html', {'form': form})

def signup(request):
    if request.method =='POST':
        print("form POST method")
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            print("post form valid")
            full_name = register_form.cleaned_data.get('full_name')
            email = register_form.cleaned_data.get('email').lower()
            phone_number = register_form.cleaned_data.get('phone_number')
            password1 = register_form.cleaned_data.get('password')
            password2 = register_form.cleaned_data.get('password2')

            print("form details printed out")
            print(full_name)
            print(email)
            print(phone_number)
            print(password1)
            print(password2)

            def verify_doesnt_exists():
                if Customuser.objects.filter(email=email).exists():
                    messages.warning(
                        request, 'This email has been used already')
                    print("email address already exists")
                    return False
                elif Customuser.objects.filter(phone_number=phone_number).exists():
                    messages.warning(
                        request, 'This phone number has already been used before')
                    print("phone_number already exists")
                    return False
                else:
                    print("verify returned True")
                    return True
                
            if password1:
                print("passwords match")
                if verify_doesnt_exists():
                    print("doesnt exist--sending mail for verification")
                    # hashed = make_password(
                    #     password1, salt=None, hasher='default')
                    try:
                        inactive_user = send_verification_email(request, register_form)
                        print("sending mail password")
                        print(inactive_user)
                        messages.success(
                        request, 'Check your mailbox to confirm your email to login...mail might be in your spam folder')

                    except Exception as e:
                        print("error message")
                        print(str(e))
                else:
                    print("function verify_doesnt_exists failed...")        
            else:
                # print("this user exists already...")
                print("passwords dont match")
                messages.warning(request, 'Passwords Don\'t Match')                
        else:
            print("post form invalid")
    else:
        print("else clause of the signup form")
        print("form sent via GET request")
        register_form = RegisterForm()
    return render(request, 'my_app/signup.html', {'register_form': register_form})


def contact(request):
    if request.method =='POST':
        contact_form = ContactForm(request.POST)
    else:
        contact_form = ContactForm()
    return render(request, 'my_app/contact.html', {'contact_form': contact_form})


@login_required()
def dashboard(request):
    user = request.user
    context = {'user': user}
    return render(request, 'my_app/dashboard.html', context)

def send_template_mail(mail_subject, mail_recipient, mail_html, btn_link, mail_header, mail_body, full_name):
    

    # button_link = "https://6521-102-90-43-173.ngrok-free.app"

    context = {
        "full_name": full_name,
        "button_link": btn_link,
        "mail_header": mail_header,
        "mail_body": mail_body

    }

    html_message = render_to_string(mail_html, context= context)
    plain_message = strip_tags(html_message)
    message = EmailMultiAlternatives(
        subject = mail_subject,
        body = plain_message,
        from_email = None,
        to = [mail_recipient]
    )

    message.attach_alternative(html_message, "text/html")
    message.send()
    print(" email message sent successfully")


@login_required()
def subscribe_monthly(request):
    amount = '1000000'
    user = request.user
    full_name = request.user.full_name
    email = request.user.email
    phone = request.user.phone_number
    # paid_status = True

    response = Transaction.initialize(amount=amount, email=email)

    ref = response['data']['reference']
    print(full_name)
    create_pay_instance = Payment.objects.create(user = user, plan_type = '1 Month', amount = amount,  status = 'Paid',
                                                    reference=ref, )

    a_url = response['data']['authorization_url']

    #code for email starts here
    

    # print("running custom email template sending")

    # my_subject = "Fairford Gym Subscription Renewal"
    # my_recipient = email

    # button_link = "https://6521-102-90-43-173.ngrok-free.app"

    # context = {
    #     "full_name": full_name,
    #     "button_link": button_link
    # }

    # html_message = render_to_string("my_app/email_renewal.html", context= context)
    # plain_message = strip_tags(html_message)
    # message = EmailMultiAlternatives(
    #     subject = my_subject,
    #     body = plain_message,
    #     from_email = None,
    #     to = [my_recipient]
    # )

    # message.attach_alternative(html_message, "text/html")
    # message.send()

    #code for email ends here

    print("email sent completely")

    return redirect(a_url)

@login_required()
def subscribe_quarterly(request):
    amount = '3000000'
    user = request.user
    full_name = request.user.full_name
    email = request.user.email
    phone = request.user.phone_number
    # paid_status = True

    response = Transaction.initialize(amount=amount, email=email)

    ref = response['data']['reference']
    print(full_name)
    create_pay_instance = Payment.objects.create(user = user, plan_type = 'Quarterly', amount = amount,  status = 'Paid',
                                                    reference=ref, )

    a_url = response['data']['authorization_url']
    return redirect(a_url)

@login_required()
def subscribe_yearly(request):
    amount = '11000000'
    user = request.user
    full_name = request.user.full_name
    email = request.user.email
    phone = request.user.phone_number
    # paid_status = True

    response = Transaction.initialize(amount=amount, email=email)

    ref = response['data']['reference']
    print(full_name)
    create_pay_instance = Payment.objects.create(user = user, plan_type = 'Yearly', amount = amount,  status = 'Paid',
                                                    reference=ref, )

    a_url = response['data']['authorization_url']
    return redirect(a_url)

@login_required()
def verify_payment(request):
    paramz = request.GET.get('trxref', 'None')
    user = request.user
    full_name = request.user.full_name
    email = request.user.email
    # phone = request.user.phone_number
    print(paramz)
    pay_queryobj = Payment.objects.all().filter(reference=paramz)
    pay_instance = Payment.objects.all().filter(reference=paramz).first()
    current_user = Customuser.objects.filter(email = email)
    details = Transaction.verify(reference=paramz)
    status = details['data']['status']
    if status == 'success':
        if pay_instance.plan_type == '1 Month':
            expiry_date = pay_instance.date_created + timedelta(days=30)
            pay_queryobj.update(paid=True, status = 'Active', expiry_date=expiry_date)
            email = request.user.email
            
            current_user.update(subscribed=True, expiry_date=expiry_date)
            
            mb = "Your payment to upgrade your fairford Monthly Gym plan was successful\nWelcome on Board. Let's rock n roll"
            send_template_mail(mail_recipient=email, mail_html="my_app/email_template.html",
                        btn_link="https://6521-102-90-43-173.ngrok-free.app/", mail_subject="Fairford Payment Plan",
                          mail_header="Payment Successful", mail_body=mb, full_name= full_name)

            messages.success(request, 'Transaction successful. Your membership status has been updated')
        elif pay_instance.product_type == 'Quarterly':
            expiry_date = pay_instance.date_created + timedelta(days=94)
            pay_queryobj.update(paid=True, status = 'Active', expiry_date=expiry_date)
            email = request.user.email
            # current_user = Customuser.objects.filter(email = email)
            current_user.update(subscribed=True, expiry_date=expiry_date)
            messages.success(request, 'Transaction successful. Your membership status has been updated')

        elif pay_instance.product_type == 'Yearly':
            expiry_date = pay_instance.date_created + timedelta(days=366)
            pay_queryobj.update(paid=True, status = 'Active', expiry_date=expiry_date)
            email = request.user.email
            # current_user = Customuser.objects.filter(email = email)
            current_user.update(subscribed=True, expiry_date=expiry_date)    
            messages.success(request, 'Transaction successful. Your membership status has been updated')

        else:
            print("incorrect payment plan unavailable")
    else:
        print(' payment not successful')

    # return redirect('home')
    return redirect('payment_success')

@login_required()
def payment_success(request):
    user = request.user
    context = {'user': user}
    return render(request, 'my_app/payment_success.html', context)

def corporate_sent(request):
    return render(request, 'my_app/corporate_sent.html')

def corporate(request):
    if request.method =='POST':
        form  = CorporateForm(request.POST)
        if form.is_valid():
            print("corporate form is valid")
            email = form.cleaned_data.get('email_address')
            full_name = form.cleaned_data.get('full_name')
            hmo = form.cleaned_data.get('hmo')
            company_name = form.cleaned_data.get('company_name')
            print("data for the hmp page")
            print(email)
            print(full_name)
            print(hmo)
            print(company_name)
            CorporateMemberRequest.objects.create(full_name = full_name, email = email, hmo=hmo, company_name = company_name )
            print("Item saved successfully")
            return redirect('corporate_sent')
        else:
            print("invalid corporate form")
    else:
        print("GET request for corporate page")
        form = CorporateForm()    
    context = {'form': form}    
    return render(request, 'my_app/corporate.html', context)


def verification_successful(request):
    context = {"mgs": "Successful verification", "link": "https://0e31-102-89-46-120.ngrok-free.app/login"}
    return render(request, 'my_app/verification_successful.html', context)



def verification_failed(request):
    context = {"mgs": "Failed verification"}
    return render(request, 'my_app/verification_failed.html' )

def resend_email(request):
    if request.method =='POST':
        form  = ResendEmailForm(request.POST)
    else:
        form = ResendEmailForm()  
    return render(request, 'my_app/resend_email.html', {'form': form})
