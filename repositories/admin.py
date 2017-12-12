from django.contrib import admin

from .models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created')
    list_filter = ['name', 'created']
    search_fields = ['name']


admin.site.register(Repository, RepositoryAdmin)
