from django.contrib import admin
from django.urls import path
from . import  views

urlpatterns = [
    path("menu",views.menu,name="menu"),
    path("mobile/Overall",views.mobile,name="index"),
    path("mobile/flipkart",views.flipkart,name="flipkart"),
    path("mobile/amazon",views.amazon,name="amazon"),
    path("tv/overall",views.tv,name="tv"),
    path("tv/flipkart",views.flipkartTV,name="tv"),
    path("tv/amazon",views.amazonTV,name="tv"),
]