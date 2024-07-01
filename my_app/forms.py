from django import forms
from django.contrib.auth.hashers import make_password
# from bootstrap_datepicker_plus import DatePickerInput
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import MyCustomuser


hmolist = ( ('No HMO Selected ', 'Select HMO'),('Axa Mansard', 'Axa Mansard'), ('Reliance', 'Reliance'), ('Avon', 'Avon'), ('Leadway', 'Leadway'), ('THT (Total health trust Ltd)', 'THT (Total health trust Ltd)'))
mirwij_list = (('To Have Fun', 'To Have Fun'), ('To Keep Fit', 'To Keep Fit'), ('To Lose Weight', 'To Lose Weight'), ('To Meet New People', 'To Meet New People'), ('Recommended By Someone', 'Recommended By Someone'))

class MyDateInput(forms.DateInput):
    input_type = 'date'
    # format = "dd/mm/yyyy",
    

class ContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
                               'placeholder': 'Full Name', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputfullname'}),
        label="")
    email_address = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputemail'}),
        label="")
    message = forms.CharField(
        widget= forms.Textarea(
            attrs={
                'placeholder': 'Message Here...', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputmessage', 'rows':'3'
            }
        ), label=""

    )
    


class LoginForm(forms.Form):
    email_address = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputemail'}),
        label="")
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password', 'class': 'form-control rounded-0 p-3', 'id': 'inputpassword'}),
        label="")

class CorporateForm(forms.Form):
    email_address = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputemail'}),
        label="")
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
                               'placeholder': 'Full Name', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputfullname'}),
        label="")
    hmo = forms.ChoiceField(choices=hmolist, label='')    
    company_name = forms.CharField(
        widget=forms.TextInput(attrs={
                               'placeholder': 'Company Name', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputfullname'}),
        label="")  

class ResendEmailForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputemail'}),
        label="")

class ProfileForm(forms.ModelForm):
     class Meta:
         model = MyCustomuser
         fields = ['address', 'date_of_birth', 'profile_pic', 'reason']


# class ProfileForm(forms.Form):
#     address =  forms.CharField(
#         widget=forms.TextInput(attrs={
#                                'placeholder': 'Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputaddress'}),
#         label="")  
#     # dob = forms.CharField(
#     #     widget=forms.DateField(attrs = {
#     #         'placeholder': 'Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputdob'
#     #     }))
#     # dob = forms.DateField(required=True, label='Date of Birth', label_suffix='DOb')
#     dob = forms.DateField(widget=MyDateInput)
#     profile_pic = forms.ImageField(
#         label='Profile Picture',
#         widget=forms.ClearableFileInput(
#             attrs={
#                 'class': 'form-control mb-2 rounded-0 p-3', 'id': 'profilepic'
#             }
#         )
#     )
#     mirwij = forms.ChoiceField(choices=mirwij_list, label='Most Important reason you joined') 

class SearchUserForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={'placeholder': 'Email Address', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputemail'}),
        label="")
    


class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Enter Password Again', 'class': 'form-control mb-4', 'id': 'inputpassword'}), label="")

    class Meta:
        model = MyCustomuser
        fields = ('username', 'full_name', 'email', 'phone_number',
                  'password', 'password2')
        # widgets = {
        #     # 'description': forms.Textarea(attrs={'cols':30, 'rows': 10}),
        #     # 'Interests': forms.CheckboxSelectMultiple,
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
        self.fields['username'].widget = forms.HiddenInput(
            attrs={'value': 'gtyyyyyy'})
        self.fields['full_name'].widget.attrs.update(
            {'class': 'form-control mb-4  rounded-0 p-3', 'placeholder': 'Full Name', 'id': 'inputfullname', })
        self.fields['email'].widget.attrs.update(
            {'placeholder': 'Email Address', 'class': 'form-control mb-4  rounded-0 p-3', 'id': 'inputemail'})
        self.fields['phone_number'].widget.attrs.update(
            {'placeholder': 'Phone Number', 'class': 'form-control mb-4  rounded-0 p-3', 'id': 'inputphonenumber'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Enter Password', 'class': 'form-control mb-4 rounded-0 p-3 ', 'id': 'inputpassword'})
        self.fields['password2'].widget.attrs.update(
            {'placeholder': 'Enter Password Again', 'class': 'form-control mb-4 rounded-0 p-3', 'id': 'inputpassword2'})

    def clean(self):
        super(forms.ModelForm, self).clean()
        # subject = self.cleaned_data['subject']
        # if subject.isspace():

        self.cleaned_data['password'] = hashed = make_password(
            self.cleaned_data['password'], salt=None, hasher='default')
        self.cleaned_data['username'] = self.cleaned_data['email']
        # self.cleaned_data['password2'] = hashed = make_password(
        #     self.cleaned_data['password2'], salt=None, hasher='default')

        return self.cleaned_data
