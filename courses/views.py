from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status, permissions
from .models import Category, Course, Lesson, Tag, User, Comment, Action, Rating, LessonView
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from .serializers import (CategorySerializer, 
                            CourseSerializer, 
                            LessonSerializer, 
                            LessonDetailSerializer, 
                            UserSerializer, 
                            CommentSerializer,
                            ActionSerializer,
                            RatingSerializer,
                            LessonViewSerializer)
from .paginator import BasePagination
from django.conf import settings
from django.db.models import F


# Create your views here.
class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = BasePagination
    
    def get_queryset(self):
        courses = Course.objects.filter(active=True)
        
        q = self.request.query_params.get('q')
        if q is not None:
            courses =  courses.filter(subject__icontains = q)
            
        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses =  courses.filter(category_id = cate_id)
            
        return courses
    
    # Url: /courses/{course_id}/lesson/?q = 
    # method: GET
    
    @action(methods=['get'], detail=True, url_path = 'lessons')
    def get_lessons(self, request, pk):
        lessons = Course.objects.get(pk=pk).lessons.filter(active=True)
        
        q = request.query_params.get('q')
        if q is not None:
            lessons  = lessons.filter(subject__icontains=q)
            
            return Response(LessonSerializer(lessons, many = True).data, status = status.HTTP_200_OK)
    


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    # url: /lessons/{lesson_id}
    # method: GET
    queryset = Lesson.objects.filter(active = True)
    serializer_class = LessonDetailSerializer
    
    def get_permissions(self):
        if self.action in ['add_comment', 'take_action', 'rate']:
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
    
    @action(methods=['post'], detail=True, url_path = 'tags')
    def add_tag(self, request, pk):
        try:
            lesson = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get('tags')
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    lesson.tags.add(t)
                    
                lesson.save()
                
                return Response(self.serializer_class(lesson).data,
                                status=status.HTTP_201_CREATED)
                
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=True, url_path="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, lesson = self.get_object(),
                                       creator=request.user)
            
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # url: /lessons/{lesson_id}/like}
    @action(methods=['post'], detail=True, url_path='like')
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = Action.objects.create(type=action_type, creator = request.user, lesson=self.get_object())
            
            return Response(ActionSerializer(action).data, status=status.HTTP_200_OK)
    
    # url: /lessons/{lesson_id}/rating/}
    @action(methods=['post'], detail= True, url_path='rating')
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except IndexError | ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating, creator = request.user, lesson=self.get_object())
            
            return Response(RatingSerializer(r).data, status=status.HTTP_200_OK)
        
    @action(methods=['get'], detail=True, url_path = 'views')    
    def inc_view(self, request, pk):
        v, created = LessonView.objects.get_or_create(lesson = self.get_object())
        v.views = F('views') + 1
        v. save()
        
        v.refresh_from_db()
        
        return Response(LessonViewSerializer(v).data, status=status.HTTP_200_OK)

    
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        
        return [permissions.AllowAny()]
        
    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data,
                        status=status.HTTP_200_OK)
        
class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            super().destroy(request, *args, **kwargs)
            
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            super().destroy(request, *args, **kwargs)
            
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    
class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)