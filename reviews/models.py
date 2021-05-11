from django.db import models

# Create your models here.
class Review_Image(models.Model):
    review_image_url = models.CharField(max_length=2000)

    class Meta: 
        db_table = 'review_images'

class Review(models.Model):
    product          = models.ForeignKey('products.Product',on_delete=models.CASCADE)
    user             = models.ForeignKey('users.User',on_delete=models.CASCADE)   
    review_image     = models.ForeignKey('Review_Image',on_delete=models.CASCADE)
    rating           = models.IntegerField()
    text             = models.CharField(max_length=2000)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'