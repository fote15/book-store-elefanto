"""
django admin customization
"""
from django.contrib import admin # noqa
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models
from book import models as BookModels
from author import models as AuthorModels


class UserAdmin(BaseUserAdmin):
    """Define admin pages for users"""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                )
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )
    readonly_fields = ['last_login']


class BookAdmin(admin.ModelAdmin):
    """Define admin pages for users"""
    ordering = ['id']
    list_display = ['title', 'rating']

    readonly_fields = ['rating']


admin.site.register(models.User, UserAdmin)
admin.site.register(BookModels.Book, BookAdmin)
admin.site.register(BookModels.BookReview)
admin.site.register(BookModels.Genre)
admin.site.register(AuthorModels.Author)
