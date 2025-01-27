from django.contrib import admin
from .models import PiPayment, User
# Register your models here.


admin.site.register(PiPayment)
admin.site.register(User)