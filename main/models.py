from django.db import models
from datetime import datetime
# Create your models here.
from django.urls import reverse


class Size(models.Model):
    title = models.CharField(max_length=200, blank=True, verbose_name="Граммы")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, blank=True, null=True, verbose_name="Категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Граммы"
        verbose_name_plural = "Граммы"


class Category(models.Model):
    title = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        result_title = self.title
        parent_model = self.parent
        while parent_model:
            result_title = parent_model.title + " --> " + result_title
            parent_model = parent_model.parent
        return result_title

    class Meta:
        verbose_name = "Категории"
        verbose_name_plural = "Категории"


class CategoryBrand(models.Model):
    title = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.category.title} --> {self.title}'

    class Meta:
        verbose_name = "Бренды"
        verbose_name_plural = "Бренды"


class Product(models.Model):
    title = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    old_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    mini_description = models.TextField(blank=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True)
    logo = models.ImageField(upload_to='upload', blank=True)
    logo2 = models.ImageField(upload_to='upload', blank=True)
    logo3 = models.ImageField(upload_to='upload', blank=True)
    logo4 = models.ImageField(upload_to='upload', blank=True)
    logo5 = models.ImageField(upload_to='upload', blank=True)
    logo6 = models.ImageField(upload_to='upload', blank=True)
    description1 = models.TextField(blank=True)
    description2 = models.TextField(blank=True)
    is_new = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    is_discount = models.BooleanField(default=False)
    brand = models.ForeignKey(CategoryBrand, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField(blank=True, default=0)
    discount = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.title


class Cart(models.Model):
    comment = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    zip_code = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_payed = models.BooleanField(default=False)
    status = models.IntegerField(default=0)  # 0 - created, -1 - declained, 1 - confirmed
    session_id = models.CharField(max_length=200, blank=True)
    amount = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    orig_price = models.FloatField(default=0)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.session_id} --> {self.last_name}'


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    price = models.FloatField(default=0)
    status = models.IntegerField(default=0)  # 0 - created, -1 - deleted
    all_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.cart.id} --> {self.product.title} --> {self.amount}'


class CompareItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(default=0)  # 0 - created, -1 - deleted

    def __str__(self):
        return f'{self.session_id}  -->  {self.product.title}'


class WishItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=200, blank=True)
    status = models.IntegerField(default=0)  # 0 - created, -1 - deleted

    def __str__(self):
        return f'{self.session_id}  -->  {self.product.title}'


class Subscriber(models.Model):
    email = models.CharField(max_length=200)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.email
