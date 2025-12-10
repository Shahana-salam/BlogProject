from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect

from blogapp.forms import CategoryForm
from blogapp.models import UserProfile, Posts


# -------------------- ADMIN DASHBOARD ---------------------
def admin_dashboard(request):
    total_users = User.objects.count()
    total_posts = Posts.objects.count()
    blocked_users = User.objects.filter(is_active=False).count()

    return render(request, "admin/admin_dashboard.html", {
        "total_users": total_users,
        "total_posts": total_posts,
        "blocked_users": blocked_users
    })


# -------------------- USER MANAGEMENT ---------------------
def admin_users(request):
    users = User.objects.all()
    return render(request, "admin/admin_users.html", {"users": users})


def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, "User blocked successfully")
    return redirect("admin_users")


def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "User unblocked successfully")
    return redirect("admin_users")


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect("admin_users")


# -------------------- POST MANAGEMENT ---------------------
def admin_posts(request):
    posts = Posts.objects.select_related('author').all()
    return render(request, 'admin/admin_posts.html', {'posts': posts})


def delete_post(request, post_id):
    post = Posts.objects.get(id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully")
    return redirect("admin_posts")


def create_Category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('admin_view')
    else:
        form = CategoryForm()

    return render(request, 'createcategory.html', {'form':form})

