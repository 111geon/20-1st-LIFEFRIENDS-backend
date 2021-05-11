from django.db import models

# Create your models here.
class User(models.Model):
    gender          = models.ForeignKey("Gender", on_delete=models.CASCADE)
    email           = models.CharField(max_length=200)
    password        = models.CharField(max_length=1000)
    name            = models.CharField(max_length=45)
    birth_date      = models.DateField()
    phone_number    = models.CharField(max_length=15)
    points          = models.IntegerField(default=0)
    coupons         = models.CharField(max_length=200, blank=True)
    
    class Meta:
        db_table = "users"

class Gender(models.Model):
    gender = models.CharField(max_length=20)

    class Meta:
        db_table = "genders"
        
class Like(models.Model):
    user    = models.ForeignKey("User", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE) 

    class Meta:
        db_table = "likes"