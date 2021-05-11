from django.db import models

# Create your models here.
class Selected_Product(models.Model):
    product                = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    order                  = models.ForeignKey('Order',on_delete=models.CASCADE)  
    quantity               = models.IntegerField()

    class Meta:
        db_table = 'selected_products'

class Order(models.Model):
    user                   = models.ForeignKey('products.Product',on_delete=models.CASCADE)   # 이건 나중에 'users.User" 로 바꿔야함 연결안시키면 엡 못만들어서 그냥 해놓은것임
    status                 = models.ForeignKey('Status',on_delete=models.CASCADE)  
    delivery_address       = models.CharField(max_length=200)
    recipient_phone_number = models.CharField(max_length=45) 
    recipient_name         = models.CharField(max_length=45)
    created_at             = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_tables = 'orders'

class Status(model.Models):
    status                 = models.CharField(max_length=20)

    class Meta:
        db_tables = 'status'