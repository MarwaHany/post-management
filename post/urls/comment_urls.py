from django.urls import path

from ..views import post_views, comment_views

urlpatterns = [
    # comments routes
    path("get-comments/", comment_views.list, name="get-comments"),
    path("get-comment-details/", comment_views.detail, name="get-comment-details"),
    path("add-comment/", comment_views.post, name="add-comment"),
    path("update-comment/", comment_views.update, name="update-comment"),
    path("delete-comment/", comment_views.delete, name="delete-comment"),
]
