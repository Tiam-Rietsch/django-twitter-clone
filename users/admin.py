from django.contrib import admin
from .models import User, Profile

class ModelAdmin(admin.ModelAdmin):
    model = User
    list_display = ['email', 'first_name', 'last_name', 'username', 'is_staff']


admin.site.register(User, ModelAdmin)
admin.site.register(Profile)
