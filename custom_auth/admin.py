from django.contrib import admin

from custom_auth.models import ExternGoogleUser


class ExternGoogleUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'extern_id', 'is_username_changed')


admin.site.register(ExternGoogleUser, ExternGoogleUserAdmin)
