from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'main.views.initial', name="initial"),
    url(r'^posts/$', 'main.views.all_posts', name="posts"),
    url(r'^posts/(?P<id>[0-9]+)/$', 'main.views.edit_post', name="edit_post"),
    url(r'^create-post/$', 'main.views.create_post', name="create_post"),
]