from django.db import models

# Create your models here.
class Menu(models.Model):
    name            = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'menus'

class Category(models.Model):
    menu            = models.ForeignKey('Menu',on_delete=models.CASCADE)
    name            = models.CharField(max_length=20)

    class Meta:
        db_table = 'categories'

class Theme(models.Model):
    menu            = models.ForeignKey('Menu',on_delete=models.CASCADE)
    name            = models.CharField(max_length=45)
    product         = models.ManyToManyField('Product',through='Theme_Product')

    class Meta:
        db_table = 'themes'

class Theme_Product(models.Model):
    theme           = models.ForeignKey('Theme',on_delete=models.CASCADE)
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)

    class Meta:
        db_table = 'themes_products'

class Product(models.Model):
    category        = models.ForeignKey('Category',on_delete=models.CASCADE)
    name            = models.CharField(max_length=50)
    cost            = models.DecimalField(max_digits=9, decimal_places=2)
    created_at      = models.DateTimeField(auto_now_add=True)
    clicks          = models.IntegerField()
    description_img = models.CharField(max_length=2000)

    class Meta: 
        db_table = 'products'

class Product_Image(models.Model):
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)
    url             = models.CharField(max_length=2000)

    class Meta:
        db_table = 'product_images'

class Size(models.Model):
    name            = models.CharField(max_length=20)
    product         = models.ManyToManyField('Product',through='Product_Size')

    class Meta:
        db_table = 'sizes'

class Product_Size(models.Model):
    product         = models.ForeignKey('Product',on_delete=models.CASCADE)
    size            = models.ForeignKey('Size',on_delete=models.CASCADE)
    quantity        = models.IntegerField()

    class Meta:
        db_table = 'products_sizes'


