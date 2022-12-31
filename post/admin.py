from django.contrib import admin

from .models import Comment, Post, User


def check_perm(user_obj):
    if user_obj.is_superuser or user_obj.is_staff:
        return True
    return False


class PostAdmin(admin.ModelAdmin):
    list_filter = ("Author__username",)
    search_fields = (
        "Author__username",
        "Body",
        "Title",
    )

    def check_perm(self, user_obj):
        if user_obj.is_superuser or user_obj.is_staff:
            return True
        return False

    def has_view_permission(self, request, obj=None):
        return check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("Author__username",)
    search_fields = ("Author__username", "Body")

    def has_view_permission(self, request, obj=None):
        return check_perm(request.user)

    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
