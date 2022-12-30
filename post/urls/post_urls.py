from django.urls import path

from ..views import post_views, comment_views

urlpatterns =[
    # post routes
    path('get-posts/',post_views.get,name="get-posts"),
    path('get-post-details/',post_views.detail,name="get-post-details"),
    path('add-post/',post_views.post,name="add-post"),
    path('update-post/',post_views.update,name="update-post"),
    path('delete-post/',post_views.delete,name="delete-post"),
]