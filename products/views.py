import json
from json import decoder
import random
from typing import Text

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
# from users.validations import Validation

class ProductView(View):
    # @Validation.validate_login
    def post(self,request,product_id):
        # user = request.account
        data    = json.loads(request.body)
        
        try: 
            product  = Product.objects.filter(id=product_id) 
            size     = product.size_set.get(name=data['product_size'])
            quantity = data['quantity']
            
            is_product      = True if product.exist() else False
            is_product_size = True if size.exist() else False

            if not is_product:    
                return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
            if not is_product_size:    
                return JsonResponse({'MESSAGE':'INVALID_SIZE'}, status=400)   

            results = {
                'product_size' : size.name,
                'product_quantity' : quantity,
                'product_in_cart'  : quantity,
                # 'user'
            }     

            return JsonResponse({'RESULTS': results}, status=200)
        
        except KeyError:
                return JsonResponse({'MESSAGE':'NEED_INPUT'}, status=400)  
            
    def get(self,request):
        product_id = request.GET.get('id', None)
        if not product_id:     
            return JsonResponse({'MESSAGE':'NOT_FOUND_ID'}, status=400)   
        if int(product_id) > Product.objects.count():
            return JsonResponse({'MESSAGE':'NOT_FOUND_PRODUCT'}, status=400)   
        
        product    = Product.objects.get(id=product_id)
        productdetail = {
            'images'           : [product_images.url for product_images in product.productimage_set.all()],
            'menu'             : product.category.menu.name,
            'category'         : product.category.name,
            'name'             : product.name,
            'cost'             : product.cost,
            'clicks'           : product.clicks,
            'description'      : product.description_iamge_url,
            'size'             : [product_size.name for product_size in product.size_set.all()]
        }
        return JsonResponse({'productdetail':productdetail}, status=200)

