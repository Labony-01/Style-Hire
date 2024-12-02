# models.py

from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('tops', 'Tops'),
        ('bottoms', 'Bottoms'),
        ('dresses', 'Dresses'),
        ('accessories', 'Accessories'),
        # Add more categories as needed
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unisex', 'Unisex'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tops')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unisex')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} in {self.cart.user.username}'s Cart"


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s Wishlist"
