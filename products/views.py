import json
from json import JSONDecodeError

from django.http     import JsonResponse
from django.views    import View

from products.models import Product
from users.validations import Validation

class ProductView(View):
    @Validation.validate_login
    def post(self,request,product_id):        
        try: 
            data     = json.loads(request.body)
            product  = Product.objects.get(id=product_id) 
            size     = product.size_set.get(name=data['product_size'])
            quantity = data['quantity']
            
            if not Product.objects.filter(id=product_id).exists():    
                return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
            if not product.size_set.filter(name=data['product_size']).exists():    
                return JsonResponse({'MESSAGE':'INVALID_SIZE'}, status=400)   
            if int(product_id) > Product.objects.count():
                return JsonResponse({'MESSAGE':'NOT_FOUND_PRODUCT'}, status=400)   
                            
            results = {
                'product_size'     : size.name,
                'product_quantity' : quantity,
                'total_price'      : int(product.cost) * int(quantity),
                'user'             : request.account.name
            }
            return JsonResponse({'RESULTS': results}, status=200)
        
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_INPUT'}, status=400)

            
    def get(self,request):
        product_id = request.GET.get('id', None)
        if not product_id:     
            return JsonResponse({'MESSAGE':'NOT_FOUND_PRODUCT_ID'}, status=400)   
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

