from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, UserViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', CustomUserViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
