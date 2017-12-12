from django.contrib import admin

from .models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_display_links = ('name',)
    list_filter = ['name', 'created']
    search_fields = ['name']


admin.site.register(Repository, RepositoryAdmin)
