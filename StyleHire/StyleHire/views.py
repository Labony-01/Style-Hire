# views.py
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, WishList, WishListItem
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from django.contrib.auth.decorators import login_required

# Admin Login View
def admin_login(request):
    print(request.method)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # Static username and password
        if username == 'admin' and password == 'admin123':
            request.session['is_admin'] = True
            print("Is Admin = ", True)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('admin_login')
    return render(request, 'admin_login.html')

# Admin Logout View
def admin_logout(request):
    try:
        del request.session['is_admin']
    except KeyError:
        pass
    messages.info(request, 'Logged out')
    return redirect('home')

# Admin Dashboard View
def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    products = Product.objects.all()
    return render(request, 'admin_dashboard.html', {'products': products})

# Admin Add Product View
def admin_add_product(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    if request.method == 'POST':
        # Handle form submission
        name = request.POST['name']
        description = request.POST['description']
        tags = request.POST['tags']
        category = request.POST['category']
        gender = request.POST['gender']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES.get('image')
        product = Product.objects.create(
            name=name,
            description=description,
            tags=tags,
            category=category,
            gender=gender,
            price=price,
            stock=stock,
            image=image,
        )
        messages.success(request, 'Product added successfully')
        return redirect('admin_dashboard')

    category_choices = Product.CATEGORY_CHOICES
    gender_choices = Product.GENDER_CHOICES
    return render(request, 'admin_add_product.html', {
        'category_choices': category_choices,
        'gender_choices': gender_choices,
    })

# Admin Edit Product View
def admin_edit_product(request, product_id):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Handle form submission
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.tags = request.POST['tags']
        product.category = request.POST['category']
        product.gender = request.POST['gender']
        product.price = request.POST['price']
        product.stock = request.POST['stock']
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('admin_dashboard')

    category_choices = Product.CATEGORY_CHOICES
    gender_choices = Product.GENDER_CHOICES
    return render(request, 'admin_edit_product.html', {
        'product': product,
        'category_choices': category_choices,
        'gender_choices': gender_choices,
    })

# Admin Delete Product View
def admin_delete_product(request, product_id):
    if not request.session.get('is_admin'):
        return redirect('admin_login')
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('admin_dashboard')

# Home View
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

# Sign-up View
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')

        # Create user
        user = User.objects.create_user(username=username, password=password)
        # Create associated Cart and Wishlist
        Cart.objects.create(user=user)
        WishList.objects.create(user=user)

        messages.success(request, 'Account created successfully.')
        return redirect('signin')

    return render(request, 'signup.html')

# Sign-in View
def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('signin')

    return render(request, 'signin.html')

# Sign-out View
def signout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

# Add to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart.objects.get(user=request.user)

    # Check if the item already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # If item exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart_detail')

# Cart Detail View
@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart_detail.html', {'items': items, 'total_price': total_price})

# Add to Wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = WishList.objects.get(user=request.user)

    # Check if the item already exists in the wishlist
    if WishListItem.objects.filter(wishlist=wishlist, product=product).exists():
        messages.info(request, f'{product.name} is already in your wishlist.')
    else:
        WishListItem.objects.create(wishlist=wishlist, product=product)
        messages.success(request, f'{product.name} added to wishlist.')

    return redirect('wishlist_detail')

# Wishlist Detail View
@login_required
def wishlist_detail(request):
    wishlist = WishList.objects.get(user=request.user)
    items = wishlist.items.all()
    return render(request, 'wishlist_detail.html', {'items': items})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Get Products by Gender
def product_list_by_gender(request, gender):
    products = Product.objects.filter(gender=gender)
    return render(request, 'product_list.html', {'products': products, 'gender': gender})
