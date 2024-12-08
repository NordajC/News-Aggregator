from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Article, Category, Comment
from django.contrib.sessions.models import Session

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'expire_date']
    readonly_fields = ['session_data']


admin.site.register(CustomUser)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)
