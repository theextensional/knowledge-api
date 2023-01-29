# https://docs.djangoproject.com/en/4.1/ref/contrib/admin/
from django.contrib import admin
from faci.models import Member, FaciCanvas


admin.site.register(Member)


class FaciCanvasAdmin(admin.ModelAdmin):
    list_display = ('id', 'aim', 'aim_type', 'user_creator')


admin.site.register(FaciCanvas, FaciCanvasAdmin)
