from django.contrib import admin
from django.urls import path, include
# from knox import views as knox_views
from .views import UserRegistrationView, UserLoginView, UserProfileView, UsercChangePasswordView, UserLogout,ShowDynamicLinks


urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UsercChangePasswordView.as_view(), name='changepassword'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('links/', ShowDynamicLinks.as_view(), name='links'),
    # path('logout/', knox_views.LogoutView.as_view(), name='logout')
]
