# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/gender/<str:gender>/', views.product_list_by_gender, name='product_list_by_gender'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
