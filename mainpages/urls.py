from django.urls import path 

from mainpages.views import *

urlpatterns = [
    path('/menus', MenuView.as_view()),
    path('/coupons/<str:coupon>', CouponView.as_view()),
    path('/search', SearchView.as_view()),
]