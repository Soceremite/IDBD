"""idbdserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include

from rest_framework.routers import DefaultRouter
from server import  views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    #path(ServerPrefix,include(ServerRouter.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/login/',views.LoginView.as_view()),
    path('api/user/autologin/',views.AutoLoginView.as_view()),
    path('api/user/register/',views.RegisterView.as_view()),
    path('api/adminuser/register/',views.AdminRegisterView.as_view()),
    path('api/adminuser/admingetuser/',views.AdminGetUserView.as_view()),
    path('api/adminuser/admindeleteuser/', views.AdminDeleteUserView.as_view()),
    path('api/user/info/',views.UserInfoView.as_view()),
    path('api/user/getstatus/',views.GetStatusView.as_view()),
    path('api/user/transportstream/',views.TransportStreamView.as_view()),
    path('api/user/getillegaldata/',views.GetIllegalDataView.as_view()),
    path('api/user/logout/',views.LogoutView.as_view()),
    path('api/user/mobile/',views.UserMobileView.as_view()),
    path('api/user/drink/',views.UserDrinkView.as_view()),
    path('api/user/smoke/',views.UserSmokeView.as_view()),
    path('api/user/tired/',views.UserTiredView.as_view()),
    path('api/user/yawn/',views.UserYawnView.as_view()),
    path('api/user/blink/',views.UserBlinkView.as_view()),
    path('api/user/deletedrink/',views.DeleteDrinkView.as_view()),
    path('api/user/deletesmoke/',views.DeleteSmokeView.as_view()),
    path('api/user/deletemobile/',views.DeleteMobileView.as_view()),
    path('api/user/deletetired/',views.DeleteTiredView.as_view()),
]
