from django.contrib import admin
from .models import Post, PostImage, HidePost


admin.site.register(Post)
admin.site.register(HidePost)
admin.site.register(PostImage)