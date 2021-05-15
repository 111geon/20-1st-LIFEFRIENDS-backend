import json
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View
from products.models import *
from users.models    import *
# Create your views here.
class MenuView(View):
    def get(self,request):
        menus    = Menu.objects.all()
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
    def get(self,request,coupon):
        is_coupon = Coupon.objects.filter(coupon=coupon).exists()
        if is_coupon:
            coupon = Coupon.objects.get(coupon=coupon).coupon
            return JsonResponse({'MESSAGE': coupon}, status=200)
        else:
            return JsonResponse({'MESSAGE': 'INVALID_COUPON'}, status=200)

class SearchView(View):
    def get(self,request):
        product_name = request.GET.get('search', None)
        if product_name:
            products = Product.objects.filter(name__contains=product_name)
        results = []
        for product in products:
            product_info = {
                'category'  : product.category.name,
                'name'      : product.name,
                'cost'      : product.cost,
                'image_url' : product.productimage_set.first().url,
                'created_at': product.created_at
            }
            results.append(product_info)

        sort = request.GET.get('sorting', None)
        if not 'sorting':
            results = sorted(
                results, 
                key = lambda product_info: product_info['name']
            )
        elif sort == 'LOWERPRICE':
            results = sorted(
                results, 
                key = lambda product_info: product_info['cost']
            )
        elif sort == 'HIGHPRICE':
            results = sorted(
                results,
                key = lambda product_info: -product_info['cost']
            )
        elif sort == 'RECENT':
            results = sorted(
                results,
                key = lambda product_info: product_info['created_at']
            )
        elif sort == 'REVIEW':
            pass
        
        Counted_sorted_products = len(results)

        return JsonResponse({'results':results, 'sorted_products': Counted_sorted_products}, status=200)