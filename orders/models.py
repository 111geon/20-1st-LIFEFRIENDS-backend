from django.db import models

# Create your models here.
class ProductOrder(models.Model):
    product                = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    order                  = models.ForeignKey('Order',on_delete=models.CASCADE)  
    quantity               = models.IntegerField()


    class Meta:
        db_table = 'products_orders'

class Order(models.Model):
    user                   = models.ForeignKey('users.User',on_delete=models.CASCADE)
    delivery_address       = models.CharField(max_length=200,blank=True) # 배송전 상태일 때 굳이 필요없음
    recipient_phone_number = models.CharField(max_length=45,blank=True) # 배송전 상태일 때 굳이 필요없음
    recipient_name         = models.CharField(max_length=45,blank=True)# 배송전 상태일 때 굳이 필요없음
    created_at             = models.DateTimeField(auto_now_add=True)
    status                 = models.ForeignKey('Status',on_delete=models.CASCADE,default=1) 

    class Meta:
        db_table = 'orders'

class Status(models.Model):
    status                 = models.CharField(max_length=20)

    class Meta:
        db_table = 'status'