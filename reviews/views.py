import json
from json import JSONDecodeError


from django.http import JsonResponse
from django.views import View

from reviews.models import ReviewImage
from products.models import Product
from orders.models  import ProductOrder
from users.validations import Validation

class ReviewImageView(View):
    def post(self,request):
        data = json.loads(request.body)
        #CreateData
        ReviewImage.objects.create(review_image_url = data['review_image_url'])
        return JsonResponse({'MASAGE':'SUCCESS'}, status=201)   

class ReviewView(View):
    @Validation.validate_login
    def post(self,request,product_id):
        data = json.loads(request.body)
        try: 
            if not Product.objects.filter(id=product_id).exists():    
                return JsonResponse({'MESSAGE':'INVALID_PRODUCT'}, status=400)  
            DELIVERED = 4 # status_id = 4(배송완료) 
            if (request.account.email) not in (ProductOrder.objects.filter(order__user__email=request.account.email)) and ProductOrder.objects.filter(status_id=DELIVERED)

            product  = Product.objects.get(id=product_id) 
            
            size     = product.size_set.get(name=data['product_size'])
            quantity = data['quantity']
            
        except: 




            product_name      = Product.objects.get(name=data['product_name'])
            product_size      = Size.objects.get(name=data['product_size'])
            products_quantity = ProductSize.objects.get(product=product_name, size=product_size)
            in_cart_products  = products_quantity.productorder_set.filter(status_id=1)
            ordered_users     = [in_cart_product.order.user.name for in_cart_product in in_cart_products]
            user              = User.objects.get(email=data['user_email'])

        if not user.name in ordered_users:
            return JsonResponse({'MASAGE':'INVAILID_USER'}, status=201)   
            
        Review.objects.create(
            rating       = data['rating'], # 1~5
            text         = data['text'],
        )
        return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)

    # def get (self,request):
    #     product_id = request.GET.get('id', None)
    #     product = Product.objects.get(id=product_id)
    #     reviews = product.review_set.all()

    #     results = []
    #     for review in reviews:
    #         review_info = {
    #             'user_name' : review.user.name,
    #             'created_at' : review.created_at,
    #             'product_size' : product.size,
    #             'text' : review.text,
    #             'review_image' : [review_images.review_image_url for review_images in review.reiewimage_set.all()],
    #             'rating' : review
    #         }
    #         results.append(review_info)
    #     return JsonResponse({'RESULTS': results}, status=201)