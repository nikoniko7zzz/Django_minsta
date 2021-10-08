from django.contrib import admin
from .models import Post, Category, Record, Test

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Record)
admin.site.register(Test)
