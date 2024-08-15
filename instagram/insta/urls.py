from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='insta'),
    path('forgotpass',views.forgotpass,name='instaforgotpass'),
    path('signup',views.signup,name='signup'),
    path('signout',views.signout,name='signout'),
    path('home',views.home,name='home'),
    path("search",views.search,name="search"),
    path("profile",views.profile,name="profile"),
    path('reels',views.reels,name='reels'),
    path('more',views.more,name='more'),
    path('create',views.create,name='create'),
    path('settings',views.settings,name='settings'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),


    # This Urls For Facebook
    
    path('facebook',views.fb ,name='instafacebook'),
    path('forgottenac',views.forgottenac,name='forgottenac'),
    path('signupforfb',views.signupforfb,name='signupforfb'),
    path('alreadyfacebookaccount',views.alreadyfbac,name='alreadyfacebookaccount'),
    path('login/', views.login_view, name='login'),
]