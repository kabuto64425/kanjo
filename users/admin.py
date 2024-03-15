from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import User

@admin.register(User)
class AdminUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "nick_name", "uuid_for_google_form")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ('uuid_for_google_form',)

#CustomUser = get_user_model()
#admin.site.register(CustomUser, AdminUserAdmin)

#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#    readonly_fields = ('uuid_for_google_form',)

