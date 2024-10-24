from django.contrib import admin
from .models import Course, Category, User, Comment, Lesson, MemberView
from django.contrib.auth.models import Permission

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(User)
admin.site.register(Lesson)
admin.site.register(Permission)
admin.site.register(MemberView)
