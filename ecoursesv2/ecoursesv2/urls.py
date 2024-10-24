"""ecoursesv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SchemaView = get_schema_view(
    openapi.Info(
      title="E-Course API",
      default_version='v1',
      description="APIs for CourseApp",
      contact=openapi.Contact(email="phamhoangphuc72@gmail.com"),
      license=openapi.License(name="Vince"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('', include('courses.urls')),
    re_path(r'^swagger(?P<format>.json|.yaml)$', SchemaView.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
