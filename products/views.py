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
        products = Product.objects.filter(name__contains=product_name)
        
        sort = request.GET.get('sort', None)
        if sort == None:
            sorted_products = products.order_by('name')

        if sort == 'LOWPRICE':
            sorted_products = products.order_by('cost')
        if sort == 'HIGHPRICE':
            sorted_products = products.order_by('-cost')
        if sort == 'RECENT':
            sorted_products = products.order_by('created_at')
        # if sort == 'REVIEW':
        #     sorted_products = products.annoate(review_count=Count()

        results = []
        for product in sorted_products:
            product_info = {
                'category'  : product.category.name,
                'name'      : product.name,
                'cost'      : product.cost,
                'image_url' : product.productimage_set.first().url,
                'created_at': product.created_at
            }
            results.append(product_info)


        count_products = len(results)

        return JsonResponse({'results':results, 'count_products': count_products}, status=200)