from django.contrib import admin
from .models import Course, Category, User, Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(User)