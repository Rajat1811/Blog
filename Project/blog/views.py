from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.core.checks import messages
from .forms import (
    PostForm,
    ProfileForm,
    RegistrationForm,
    LoginForm,
    EditProfileForm,
    CommentForm,
)
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    SetPasswordForm,
)
from .models import Profile, Post, Comment, Like
from django.contrib.auth.models import User
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(
        request,
        "blog/home.html",
    )


# Register
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "blog/registration.html", {"form": form})


# Login
def user_login(request):
    if request.method == "POST":
        fm = LoginForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data["username"]
            upass = fm.cleaned_data["password"]
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect("emp_home")
    else:
        fm = LoginForm()
    return render(request, "blog/login.html", {"form": fm})


# Logout
def user_logout(request):
    logout(request)
    return redirect("login")


# Home
def home(request):
    if request.user.is_authenticated:
        user = request.user
        detail = Profile.objects.get(user_id=request.user.id)
        print(detail)
        return render(request, "blog/emp_home.html", {"user": user, "detail": detail})
    else:
        return redirect("login")


# Profile
def create_profile(request):
    if request.method == "POST":
        profile = Profile(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("emp_home")
    else:
        form = ProfileForm()
    return render(request, "blog/create_profile.html", {"form": form})


def update_profile(request):
    img = get_object_or_404(Profile, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            return redirect("emp_home")
        else:
            print(form.errors)
    else:
        form = ProfileForm(instance=img)
    return render(request, "blog/update_profile.html", {"form": form})


def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditProfileForm(request.POST, instance=request.user)
            if form.is_valid:
                form.save()
                return redirect("emp_home")
        else:
            form = EditProfileForm(instance=request.user)
        return render(request, "blog/edit_profile.html", {"form": form})
    else:
        return redirect("login")


# Post
def create_post(request):
    if request.method == "POST":
        post = Post(user=request.user)
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("emp_home")
        else:
            print(form.errors)
    else:
        form = PostForm()
    return render(request, "blog/create_post.html", {"form": form})


def my_post(request, data=None):
    if data == None:
        detail = Post.objects.filter(user_id=request.user)
    elif data == "published":
        detail = Post.objects.filter(user_id=request.user, is_published=True)
    elif data == "unpublished":
        detail = Post.objects.filter(user_id=request.user, is_published=False)
    return render(request, "blog/my_post.html", {"detail": detail})


def all_post(request):
    detail = Post.objects.all().order_by("on_published")
    paginator = Paginator(detail, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/all_post.html", {"page_obj": page_obj})


def edit_post(request, pk):
    obj = get_object_or_404(Post, id=pk, user=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("my_post")
        else:
            print(form.errors)
    else:
        form = PostForm(instance=obj)
    return render(request, "blog/edit_post.html", {"form": form})


def delete_post(request, pk):
    obj = get_object_or_404(Post, id=pk, user=request.user)
    if request.method == "POST":
        obj.delete()
        return redirect("my_post")
    return render(request, "blog/delete_post.html")


def detailview(request, pk):
    obj = get_object_or_404(Post, id=pk)
    detail = Comment.objects.filter(post=obj)
    return render(request, "blog/detailview.html", {"obj": obj, "detail": detail})


# Comment
def add_comment(request, pk):
    try:
        data = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404("Data does not exist")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Com = Comment(body=form.cleaned_data["body"], user=request.user, post=data)
            Com.save()
            return redirect(f"/blog/detailview/{pk}")
    else:
        form = CommentForm()
    return render(request, "blog/comment.html", {"form": form})


# Search
def search(request):
    query = request.GET["query"]
    q1 = Post.objects.filter(title__icontains=query)
    q2 = Post.objects.filter(description__icontains=query)
    q3 = Post.objects.filter(user__username__icontains=query)
    detail = q1.union(q2, q3)
    return render(request, "blog/search.html", {"detail": detail})


# Change Password
def change_pass(request):
    if request.method == "POST":
        fm = SetPasswordForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request, fm.user)
            return redirect("http://127.0.0.1:8000/employee/emp_home/")
    else:
        fm = SetPasswordForm(user=request.user)
    return render(request, "blog/changepass.html", {"form": fm})


# Like
def like_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        post_obj = Post.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        like.save()
    return redirect("all_post")
