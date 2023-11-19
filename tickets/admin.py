from django.contrib import admin

from .models import Ticket, Tech

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Tech)