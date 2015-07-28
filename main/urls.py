from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', 'main.views.initial', name="initial"),
    url(r'^login/$', 'main.views.login', name="login"),
    url(r'^logout/$', 'main.views.logout', name="logout"),
    url(r'^post-admin/$', 'main.views.post_admin', name="post_admin"),
    url(r'^posts/$', 'main.views.all_posts', name="posts"),
    url(r'^post-previews/$', 'main.views.post_previews', name="post_previews"),
    url(r'^bootstrap/$', 'main.views.bootstrap', name="bootstrap"),
    url(r'^posts/(?P<id>[0-9]+)/$', 'main.views.edit_post', name="edit_post"),
    url(r'^posts/(?P<id>[0-9]+)/json/$', 'main.views.post_json', name="post_json"),
]
