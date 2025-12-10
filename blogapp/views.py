import random

from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from blogapp.models import Posts, Comment

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import PostForm, CategoryForm, CommentForm
from .models import UserProfile


def Register_user(request):

    if request.method == "POST":

        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password1')
        profile_pic = request.FILES.get('profile_pic')
        phone_number = request.POST.get('phone_number')

        # Check password match
        if password != password2:
            messages.info(request, 'Passwords do not match')
            return redirect('register')

        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register')

        # Check email exists
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Create profile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            profile_pic=profile_pic
        )

        messages.success(request, "Registration Successful! Please login.")
        return redirect('user_login')

    return render(request, 'register.html')





ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect('admin_dashboard')
        else:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
              auth.login(request, user)
              return redirect('user_view')
            # USER LOGIN
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('user_login')



    return render(request, 'login.html')



def User_view(request):
    posts = Posts.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)

    except EmptyPage:
        page = paginator.page(paginator.num_pages)



    return render(request, 'user_view.html', {'posts':posts, 'page':page})


def search_post(request):
    query = None
    posts = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        posts = Posts.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query) |   # category search fixed
            Q(author__username__icontains=query)   # optional: search by author
        ).distinct()
    else:
        books = []

    context = {'posts': posts, 'query': query}
    return render(request, 'search.html', {'posts': posts, 'query': query})



def logout_user(request):
    logout(request)
    return redirect('user_login')



def createPost(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('user_view')
    else:
        form = PostForm()

    return render(request, "createpost.html", {"form": form})


def create_Category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('admin_view')
    else:
        form = CategoryForm()

    return render(request, 'createcategory.html', {'form':form})







def my_profile(request):

    # Get user profile (if using custom Profile model)
    profile = UserProfile.objects.get(user=request.user)

    # Get only this user's posts
    my_posts = Posts.objects.filter(author=request.user).order_by('-created_at')

    context = {
        'profile': profile,
        'my_posts': my_posts,
    }
    return render(request, 'my_profile.html', context)


def edit_post(request, post_id):
    post = Posts.objects.get(id=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.author = request.user  # keep original author
            updated_post.save()
            return redirect('my_profile')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


def delete_posts(request,post_id):
    posts = Posts.objects.get(id=post_id)

    if request.method == 'POST':
        posts.delete()

        return redirect('my_profile')

    return render(request,'deletepost.html',{'posts':posts})



def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update profile fields
        profile.phone_number = request.POST.get('phone_number')

        if request.FILES.get('profile_pic'):
            profile.profile_pic = request.FILES.get('profile_pic')

        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('my_profile')

    context = {
        'profile': profile,
    }
    return render(request, 'update_profile.html', context)






def post_comments(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')  # latest first

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post_comments', post_id=post.id)
        else:
            return redirect('login')  # redirect if user is not logged in
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'comment.html', context)



def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.user:
        return HttpResponse("Not allowed!")  # prevent others from editing

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_comments', post_id=comment.post.id)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form, 'comment': comment})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user == comment.user:
        comment.delete()

    return redirect('post_comments', post_id=comment.post.id)



def get_comments(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    comments = post.comments.all()

    data = []
    for c in comments:
        data.append({
            "id": c.id,
            "text": c.text,
            "user": c.user.username,
            "created_at": c.created_at.strftime("%Y-%m-%d %H:%M"),
            "can_edit": request.user == c.user
        })

    return JsonResponse({"comments": data})


def load_comments(request, post_id):
    comments = Comment.objects.filter(post_id=post_id).select_related("user")

    data = {
        "comments": [{"user": c.user.username, "text": c.text} for c in comments]
    }
    return JsonResponse(data)


def post_list(request):
    # This query fetches ALL posts AND calculates the comment_count for each
    posts = Posts.objects.annotate(
        comment_count=Count('comments')  # <-- Change this!
    ).order_by('-created_at')

    context = {
        'posts': posts
    }
    return render(request, 'user_view.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Redirect to reset page for that user
            return redirect('reset_password', email=email)
        except User.DoesNotExist:
            messages.error(request, "No registered user with this email.")
    return render(request, 'forgot_password.html')





def reset_password(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('forgot_password')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        else:
            user.set_password(password1)
            user.save()
            messages.success(request, "Password reset successful!")
            return redirect('user_login')  # Redirect to login page

    return render(request, 'reset_password.html', {'email': email})

def entry_page(request):
    return render(request, 'both_viewpage.html')