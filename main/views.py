from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import serializers
from main.models import Post
from main.forms import PostForm
import time
import json


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

    # import pdb; pdb.set_trace()

    start = page * page_size
    end = (page + 1) * page_size

    posts = Post.objects.all().order_by('-date_posted')[start:end]

    return render(request, 'post-preview.html', {'posts': posts})


def post_admin(request):

    return render(request, 'post-admin.html', {})


def create_post(request):

    form = PostForm(request.POST, request.FILES)

    if form.is_valid():
        post = form.save()
        message = "Your post has been saved"
    else:
        message = form.errors

    return render(request, 'post-admin.html', {"message": message})


def edit_post(request, id):

    if request.method == 'DELETE':

        Post.objects.get(id=id).delete()

        return HttpResponse(status=204)

    elif request.method == 'GET':

        post = Post.objects.get(id=id)

        return render(request, 'post.html', {'post': post})

def bootstrap(request):

    return render(request, 'bootstrap.html', {})
