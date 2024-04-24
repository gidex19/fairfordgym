from django.contrib import admin

from .models import MyCustomuser, Payment, CorporateMemberRequest
# Register your models here.


class MyCustomuserAdmin(admin.ModelAdmin):
    search_fields = ('email', )

admin.site.register(MyCustomuser, MyCustomuserAdmin)
admin.site.register(Payment )
admin.site.register(CorporateMemberRequest)
