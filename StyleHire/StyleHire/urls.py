# urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Existing paths...
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    # User authentication
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('signout/', views.signout_view, name='signout'),
    # Product views
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('products/gender/<str:gender>/', views.product_list_by_gender, name='product_list_by_gender'),
    # Cart and Wishlist
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_detail, name='wishlist_detail'),
    # Admin paths
    path('dashboard/login/', views.admin_login, name='admin_login'),
    path('dashboard/logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/product/add/', views.admin_add_product, name='admin_add_product'),
    path('dashboard/product/edit/<int:product_id>/', views.admin_edit_product, name='admin_edit_product'),
    path('dashboard/product/delete/<int:product_id>/', views.admin_delete_product, name='admin_delete_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
