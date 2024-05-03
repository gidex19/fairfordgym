from django.contrib import admin

from .models import MyCustomuser, Payment, CorporateMemberRequest, ContactMessage
# Register your models here.


class MyCustomuserAdmin(admin.ModelAdmin):
    search_fields = ('email', )

admin.site.register(MyCustomuser, MyCustomuserAdmin)
admin.site.register(Payment )
admin.site.register(CorporateMemberRequest)
admin.site.register(ContactMessage)
