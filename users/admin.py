from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_display_links = ('username',)
    list_filter = ['username', 'email']
    search_fields = ['username']


admin.site.register(User, UserAdmin)
