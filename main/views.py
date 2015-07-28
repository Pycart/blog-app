from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from main.models import Post
from main.forms import PostForm
from main.auth_utils import is_employee
import time
import json


def login(request):

    if request.user.is_authenticated():

        if is_employee(request.user):
            return redirect('post_admin')
        else:
            return redirect('initial')

    context = {"user_create_form": UserCreationForm()}

    if request.method == 'POST':

        if request.POST['type'] == 'login':

            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)

                    if is_employee(user):
                        return redirect('post_admin')
                    else:
                        return redirect('initial')

                else:
                    context['error'] = 'This account has been disabled'
                    return render(request, 'login.html', context)
            else:
                context['error'] = 'Invalid username or password'
                return render(request, 'login.html', context)
        else:

            full_user_create_form = UserCreationForm(request.POST)

            if full_user_create_form.is_valid():
                user = full_user_create_form.save()

                group = Group.objects.get(name="Users")
                group.user_set.add(user)

                user = authenticate(username=user.username, password=request.POST['password1'])
                auth_login(request, user)

                return redirect('initial')
            else:
                context['user_create_form'] = full_user_create_form
                context['error_on_create'] = True

    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')


def initial(request):

    return render(request, 'index.html', {})


def all_posts(request):

    posts = Post.objects.all().order_by('-date_posted')

    post_json = serializers.serialize('json', posts)

    return HttpResponse(post_json, content_type="application/json")

    # return render(request, 'posts.html', {'posts': posts})


def post_previews(request):

    page = int(request.GET.get('page', 0))
    page_size = 3

    start = page * page_size
    end = (page + 1) * page_size

    posts = Post.objects.all().order_by('-date_posted')[start:end]

    if len(posts) > 0:

        return render(request, 'post-preview.html', {'posts': posts})
    else:
        return HttpResponse('')


@login_required
@user_passes_test(is_employee)
def post_admin(request):

    posts = Post.objects.all().order_by('-date_posted')

    context = {"posts": posts}

    if request.method == 'POST':

        id = request.POST.get('id')

        if id:

            post = Post.objects.get(id=id)
            form = PostForm(request.POST, request.FILES, instance=post)

        else:

            form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save()
            context['message'] = "Your post has been saved"
        else:
            context['message'] = form.errors

    return render(request, 'post-admin.html', context)


@login_required
@user_passes_test(is_employee)
def post_json(request, id):

    post = Post.objects.get(id=id)

    post_json = serializers.serialize('json', [post])

    return HttpResponse(post_json, content_type="application/json")


def edit_post(request, id):

    if request.method == 'DELETE':

        Post.objects.get(id=id).delete()

        return HttpResponse(status=204)

    elif request.method == 'GET':

        post = Post.objects.get(id=id)

        return render(request, 'post.html', {'post': post})


def bootstrap(request):

    return render(request, 'bootstrap.html', {})
