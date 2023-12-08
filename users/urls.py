from  django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('',UserViewSet,basename='user')



urlpatterns = [
    path('signup/',UserSignUpAPIView.as_view(),name='signup'),
    path('login/', CustomLoginUserAPIView.as_view(), name='user_login'),
    path('user/', include(router.urls)),
    path('change-password/',ChangePasswordAPIView.as_view(), name='change_password')
]