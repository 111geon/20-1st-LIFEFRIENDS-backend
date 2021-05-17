from django.db import models

# Create your models here.
class ReviewImage(models.Model):
    review_image_url = models.URLField(max_length=2000)
    review           = models.ForeignKey('Review',on_delete=models.CASCADE)

    class Meta: 
        db_table = 'review_images'

class Review(models.Model):
    product_order    = models.ForeignKey('orders.ProductOrder',on_delete=models.CASCADE)
    order            = models.ForeignKey('orders.Order',on_delete=models.CASCADE)   
    rating           = models.IntegerField()
    text             = models.CharField(max_length=2000)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
