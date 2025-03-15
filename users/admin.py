from django.contrib import admin

from .models import CustomUser, Payment, Subscription

admin.site.register(CustomUser)
admin.site.register(Payment)
admin.site.register(Subscription)
