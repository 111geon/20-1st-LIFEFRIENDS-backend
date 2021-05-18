import json
import random
from typing import Text

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Count

from products.models import Product

class SearchView(View):
    def get(self,request):
        product_name = request.GET.get('search')
        products = Product.objects.filter(name__contains=product_name)
        try: 
            sort = request.GET.get('sort', None)
            if sort is None:
                sorted_products = products.order_by('name')
            if sort == 'LOWPRICE':
                sorted_products = products.order_by('cost')
            if sort == 'HIGHPRICE':
                sorted_products = products.order_by('-cost')
            if sort == 'RECENT':
                sorted_products = products.order_by('created_at')
            if sort == 'REVIEW':
                a =Product.objects.filter(name__contains='쿠션')
                sorted_products = a.annotate(count_review=Count('productsize__review')).order_by('count_review')

            product_info = [{
                'category'  : product.category.name,
                'name'      : product.name,
                'cost'      : product.cost,
                'image_url' : product.productimage_set.first().url,
                'created_at': product.created_at
            } for product in sorted_products]
            
            return JsonResponse({'results':product_info}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KeyError'}, status=200)
