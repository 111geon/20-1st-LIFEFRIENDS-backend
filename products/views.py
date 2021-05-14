import json
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View
from products.models import *
from users.models    import *
from reviews.models  import *
# Create your views here.
class MenuView(View):
    def get(self,request):
        menus = Menu.objects.all()
        MenuList = []
        for menu in menus:
            themes    = menu.theme_set.all()
            ThemeList = []
            for theme in themes:
                if theme.name != menu.name: # 메뉴이름과 테마이름이 다를때만 넣어라(메뉴,테마이름이 같은 NEW, 선물추천을 걸러줄라고 넣은것)
                    theme_info = {
                        'categoryId'  : theme.id,
                        'categoryName': theme.name,
                    }
                    ThemeList.append(theme_info)
            categories   = menu.category_set.all()
            CategoryList = []
            for category in categories:
                category_info = {
                    'categoryId'   : category.id,
                    'categoryName' : category.name,
                }
                CategoryList.append(category_info)
            menu_info = {
                'menuId'           : menu.id,
                'menuName'         : menu.name,
                'categoryList'     : CategoryList+ThemeList
            }
            MenuList.append(menu_info)
            themes = menu.theme_set.all()
            ThemeList = []
        
        return JsonResponse({'results':MenuList}, status=200)

class CouponView(View):
    def get(self,request):
        results = []
        coupon = Coupon.objects.get(coupon="15%")
        coupon_info = {
            'coupon' : coupon.coupon
        }
        results.append(coupon_info)
        return JsonResponse({'results':results}, status=200)

class ProductView(View):
    def get(self,request):
        product_id = request.GET.get('product_id', None)
        product    = Product.objects.get(id=product_id)
        producList = []
        reviews  = product.review_set.all()
        reviewsLIst = []
        for review in reviews:
            Review_info = {
                'user' : review.user,
                'review_image' : review.review_image.review_image_url,
                'rating' : review.rating,
                'text' : review.text,
                'date' : review.crated_at,
            }
            reviewsLIst.append(Review_info)
        SpecificProduct_info = {
            'menu' : product.category.menu.name,
            'category' : product.category.name,
            'name' : product.name,
            'cost' : product.cost,
            'clicks' : product.clicks,
            'description' : product.description_iamge_url,
            'reviews' : reviewsLIst
        }
        producList.append(SpecificProduct_info)
        return JsonResponse({'results':producList}, status=200)