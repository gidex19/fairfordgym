from django.contrib import admin

from .models import MyCustomuser, Payment, CorporateMemberRequest, ContactMessage
# Register your models here.


class MyCustomuserAdmin(admin.ModelAdmin):
    search_fields = ('email', 'full_name')
    list_filter = ["subscribed", "is_active", "is_corporate_user"]
    list_display = ["email", "full_name", "phone_number", "subscribed" ]

admin.site.register(MyCustomuser, MyCustomuserAdmin)
admin.site.register(Payment )
admin.site.register(CorporateMemberRequest)
admin.site.register(ContactMessage)


admin.site.site_header = 'FAIRFORD GYM ADMIN DASHBOARD'
admin.site.index_title = 'Gym Manager'
admin.site.site_title = 'Fairford Gym Admin'
