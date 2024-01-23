"""
URL configuration for echo_post_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views.signup import SignupViewSet
from rest_framework.routers import DefaultRouter

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog.views.signup import SignupViewSet, EmailVerificationViewSet
from blog.views.login import LoginViewSet
from blog.views.post import (
    PostAPIView,
    ViewAPostAPIView,
    ViewBlogPostsAPIView,
    UpdateBlogPostAPIView,
    DeleteBlogPostAPIView
)
from rest_framework.routers import DefaultRouter

# Router for auth/ namespace
auth_router = DefaultRouter()
auth_router.register(r'signup', SignupViewSet, basename='signup')
auth_router.register(r'verify-email', EmailVerificationViewSet, basename='verify-email')
auth_router.register(r'login', LoginViewSet, basename='login')

# # Router for create-blogpost/ endpoint
# blogpost_router = DefaultRouter()
# blogpost_router.register(r'create-blogpost', PostViewSet, basename='create-blogpost')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_router.urls)),
    path('create-blogpost/', PostAPIView.as_view(), name='create-blogpost'),
    path('post/<uuid:post_id>', ViewAPostAPIView.as_view()),
    path('posts', ViewBlogPostsAPIView.as_view()),
    path('update-post/<uuid:post_id>', UpdateBlogPostAPIView.as_view()),
    path('delete-post/<uuid:post_id>', DeleteBlogPostAPIView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
