from django.contrib import admin

from .models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Repository, RepositoryAdmin)
