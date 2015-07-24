from django.contrib import admin
from main.models import Post, Comment, Upload, Tag

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Upload)
admin.site.register(Tag)
