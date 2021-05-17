import json
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View
from products.models import *
# Create your views here.

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