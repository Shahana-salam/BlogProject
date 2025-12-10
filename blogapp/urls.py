from django.contrib.auth import views as auth_views
from . import views
from django.urls import path



urlpatterns = [
    path('',views.entry_page,name='entry'),
    path('register/',views.Register_user,name='register'),
    path('userlogin/',views.login_user,name='user_login'),
    path('user_view/',views.User_view,name='user_view'),
    path('search/',views.search_post,name='search'),
    path('logout/',views.logout_user,name='logout'),
    path('createpost/',views.createPost,name='create_post'),

    path('profile/',views.my_profile, name='my_profile'),
    path('editposts/<int:post_id>/',views.edit_post,name='edit_posts'),
    path('deleteposts/<int:post_id>/',views.delete_posts,name='delete_posts'),
    path('updateprofile/',views.update_profile,name='update_profile'),
    path("comment/", views.get_comments, name="comment"),
    path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("load-comments/<int:post_id>/", views.load_comments, name="load_comments"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:email>/', views.reset_password, name='reset_password'),


]

