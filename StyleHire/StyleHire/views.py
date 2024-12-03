# views.py
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product, OrderItem, Order, Contact
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

def home(request):
    # Fetch all products
    all_products = Product.objects.all()

    # Fetch new arrivals (you can define what "new arrivals" means)
    new_arrivals = Product.objects.order_by('-created_at')[:10]  # Last 10 added products

    # Fetch best-selling items (you may need to track sales to get this data)
    # For now, let's assume best sellers are products with the highest stock (as a placeholder)
    best_sellers = Product.objects.order_by('-stock')[:10]

    # Fetch bridal dresses
    bridal_dresses = Product.objects.filter(category='bridal')

    context = {
        'products': all_products,
        'new_arrivals': new_arrivals,
        'best_sellers': best_sellers,
        'bridal_dresses': bridal_dresses,
    }
    return render(request, 'home.html', context)

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
    items = cart.items.select_related('product').all()
    total_price = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        # Handle the purchase process
        # Collect contact details, address, and payment method from the form
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        # Create an Order
        order = Order.objects.create(
            user=request.user,
            contact_name=contact_name,
            contact_email=contact_email,
            shipping_address=shipping_address,
            payment_method=payment_method,
            total_price=total_price,
        )

        # Create OrderItems
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            # Optionally, reduce stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear the cart
        cart.items.all().delete()

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_success')

    return render(request, 'cart_detail.html', {'items': items, 'total_price': total_price})


@login_required
def update_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            if action == 'increment':
                cart_item.quantity += 1
                cart_item.save()
            elif action == 'decrement':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})

            return JsonResponse({
                'status': 'success',
                'quantity': cart_item.quantity if cart_item.id else 0,
                'item_total_price': cart_item.product.price * cart_item.quantity if cart_item.id else 0,
                'cart_total_price': sum(
                    item.product.price * item.quantity for item in CartItem.objects.filter(cart__user=request.user))
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item does not exist'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def order_success(request):
    return render(request, 'order_success.html')


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

def shop_view(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

# Gents View - shows products for male
def gents_view(request):
    products = Product.objects.filter(gender='male')
    return render(request, 'gents.html', {'products': products})

# Ladies View - shows products for female
def ladies_view(request):
    products = Product.objects.filter(gender='female')
    return render(request, 'ladies.html', {'products': products})

# Contact View
def contact_view(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message_text = request.POST.get('message')

        # Validate form data (you can add more validation as needed)
        if not name or not email or not message_text:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('contact')

        # Save the contact message
        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text,
        )

        # Display a success message
        messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'contact.html')

# Wishlist Detail View - updated URL name
@login_required
def wishlist_detail(request):
    wishlist = WishList.objects.get(user=request.user)
    items = wishlist.items.all()
    return render(request, 'wishlist.html', {'items': items})

# Product Detail View
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Get Products by Gender
def product_list_by_gender(request, gender):
    products = Product.objects.filter(gender=gender)
    return render(request, 'product_list.html', {'products': products, 'gender': gender})
