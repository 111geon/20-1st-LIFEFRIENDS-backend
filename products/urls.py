from django.urls import path 

from products.views import *

urlpatterns = [
    path('/mainpage/menus', MenuView.as_view()),
    path('/mainpage/coupons', CouponView.as_view()),
    path('', ProductView.as_view()),
]