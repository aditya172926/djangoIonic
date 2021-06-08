from django.urls import include, path
from rest_framework import routers
from api import views
from django.contrib.auth.models import User


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.CustomObtainAuthToken.as_view()),
    path('register/', views.RegisterApi.as_view()),
    path('logout/', views.userLogout),
]