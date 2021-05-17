# import json

# from django.http import JsonResponse
# from django.views import View
# from reviews.models import *
# from products.models import *
# from users.models import User
# from orders.models import *
# # Create your views here.
# class OrderView(View):
#     def post(self,request):
#         data = json.loads(request.body)
#         user = User.objects.get(email=data['email'])
#         status = Status.objects.get(status=data['status'])
#         #CreateData
#         order_info = Order.objects.create (
#             user = user,
#             delivery_address = data['delivery_address'],
#             recipient_phone_number = data['recipient_phone_number'],
#             recipient_name = data['recipient_name'],
#             status = status
#         )
#         return JsonResponse({'MASSAGE':'SUCCESS'}, status=201)

# class ProductOrderView(View):
#     def post(self,request):
#         data = json.loads(request.body)
#         user = User.objects.get(email=data['email'])

#         order = Order.objects.get(user=user, created_at=data['created_at'])
#         product = Product.objects.get(name=data['name'])

#         ProductOrder_info = ProductOrder.objects.create(
#             product = product,
#             order = order,
#             quantity = data['quantity']
#         )

#         if ProductOrder_info:
#             status = Status.objects.get(status=data['status'])
