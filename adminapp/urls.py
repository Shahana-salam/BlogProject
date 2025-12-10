from . import views
from django.urls import path

# Create your views here.


urlpatterns = [

path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    # USER MANAGEMENT
    path("admin/users/", views.admin_users, name="admin_users"),
    path("admin/users/block/<int:user_id>/", views.block_user, name="block_user"),
    path("admin/users/unblock/<int:user_id>/", views.unblock_user, name="unblock_user"),
    path("admin/users/delete/<int:user_id>/", views.delete_user, name="delete_user"),

    # POST MANAGEMENT
    path("admin/posts/", views.admin_posts, name="admin_posts"),
    path("admin/posts/delete/<int:post_id>/", views.delete_post, name="delete_post"),
path('create_category/',views.create_Category,name='create_category'),
]

