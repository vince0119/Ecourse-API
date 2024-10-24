from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register("category", views.CategoryViewSet, 'category')
router.register('courses', views.CourseViewSet, 'course')
# router.register('lesson', views.LessonView, 'baihoc')
router.register('lessons', views.LessonViewSet, 'lesson')
router.register('users', views.UserViewSet, 'user')
router.register('comments', views.CommentViewSet, 'comment')
router.register('members', views.MemberViewSet, 'member')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]