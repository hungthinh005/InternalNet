from django.contrib import admin

# Register your models here.

from .models import Function, Topic, Message
admin.site.register(Function)
admin.site.register(Topic)
admin.site.register(Message)