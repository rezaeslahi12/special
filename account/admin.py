from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from . models import Relation,Profile


class Profileinline(admin.StackedInline):
    model = Profile
    can_delete = False
class ExtendedUserAdmin(UserAdmin):
    inlines = (Profileinline,)

admin.site.unregister(User)
admin.site.register(User,ExtendedUserAdmin)





admin.site.register(Relation)
