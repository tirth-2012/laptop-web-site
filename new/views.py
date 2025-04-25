from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,Brand,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings

# Create your views here.

RAZORPAY_KEY_ID = "rzp_test_5gCYsNdsT8fMyh"
RAZORPAY_KEY_SECRET = "YI8yyHjIzfcrip4BvUpO7uDm"

def register(request):
    if  request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Password do not match!")
            return redirect(register)
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists!')
            return redirect(register)
        
        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()
        messages.success(request,'Account created successfully! Please log in.')
        return redirect(login_user)
    
    return render(request,'register.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            messages.error(request, "Invalid username or password!")
            return redirect(login_user)

    return render(request, "login.html")

def logout_user(requset):
    logout(requset)
    return redirect(index)

def index(request):
    products = Product.objects.all()
    brand = Brand.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
    return render(request,'index.html',{
        'brand':brand,
        'products': products,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
        })

def viewproduct(request,pk):
    product = get_object_or_404(Product, pk=pk)
    brand = Brand.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
    return render(request,'viewproduct.html',{
        'product': product,
        'brand':brand,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
    })
    
def productcategory(request,pk):
    brands = get_object_or_404(Brand, pk=pk)  # Get category
    brand = Brand.objects.all()
    print(brands)
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
    products = Product.objects.filter(brand=brands)
    return render(request,'productcategory.html',{
        'products':products,
        'brands':brands,
        'brand':brand,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
        })

def addtocart(request,pk):
    cart = request.session.get('cart', {})
    
    if str(pk) in cart:
        cart[str(pk)]['quantity'] += 1
    else:
        product = get_object_or_404(Product, pk=pk)
        cart[str(pk)] = {
            'name':product.name,
            'modelname':product.modelname,
            'price': int(product.price),
            'image': product.image1.url,
            'quantity': 1,
        }
        
    request.session['cart'] = cart
    messages.success(request, "added to cart successfully!")
    
    referer_url = request.META.get('HTTP_REFERER', '')

    if referer_url:
        return redirect(referer_url)
    else:
        return redirect(index)
    
def removefromcart(request, pk):
    """Remove a product from the cart"""
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
    request.session['cart'] = cart
    
    referer_url = request.META.get('HTTP_REFERER', '')
    
    if referer_url:
        return redirect(referer_url)
    else:
        return redirect(index)
    
def viewcart(request):
    brand = Brand.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
    return render(request,'viewcart.html',{
        'brand':brand,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
    })
    
def update_cart(request, pk, action):
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        if action == "increase":
            cart[str(pk)]['quantity'] += 1  # Increase quantity
        elif action == "decrease":
            if cart[str(pk)]['quantity'] > 1:
                cart[str(pk)]['quantity'] -= 1  # Decrease quantity
            else:
                del cart[str(pk)]
    else:
            cart[pk] = {'quantity': 1}

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('viewcart')

@login_required(login_url='login')
def checkout(request):
    brand = Brand.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
        full_name = email = phone_number = house_society_name = ""
        landmark_area = city = state = pin_code = ""
        
    if request.method == "POST":
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email", "")
        phone_number = request.POST.get("phone_number", "")
        house_society_name = request.POST.get("house_society_name", "")
        landmark_area = request.POST.get("landmark_area", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        pin_code = request.POST.get("pin_code", "")

        if not cart_items:
            messages.error(request, "Your cart is empty.")
            return redirect("checkout")

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            house_society_name=house_society_name,
            landmark_area=landmark_area,
            city=city,
            state=state,
            pin_code=pin_code,
            total_price=total_price,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                name=item["name"],
                modelname=item["modelname"],
                quantity=item["quantity"],
                price=item["price"],
                image=item["image"]
            )
        return redirect("payment")
                 
    return render(request,'checkout.html',{
        'brand':brand,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
        })
    
@csrf_exempt
def paymentrazor(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    price = int(total_price*100)
    
    data = {
        "amount": price,  # Amount in paise (₹500)
        "currency": "INR",
        "payment_capture": 1  # Auto capture
    }
    order = client.order.create(data)

    return render(request, "payment.html", {"order_id": order["id"], "razorpay_key": settings.RAZORPAY_KEY_ID})

@csrf_exempt
def payment_success(request):
    request.session['cart'] = {}  # Clear cart after successful payment
    return redirect("success")

def success(request):
    brand = Brand.objects.all()
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, item in cart.items():
        try:
            price = int(float(item['price']))  # Convert price to float first, then int
            quantity = int(item['quantity'])  # Convert quantity to integer
        except (ValueError, TypeError):
            price = 0
            quantity = 0

        item_total = price * quantity  # Multiply price * quantity
        total_price += item_total  # Add to total cart price

        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'modelname':item['modelname'],
            'price': price,
            'image': item.get('image', 'default_image.jpg'),  # Use default if missing
            'quantity': quantity,
            'total': item_total,  # Store subtotal
        })
        
    return render(request,'success.html',{
        'brand':brand,
        'cart_items': cart_items,
        'cart_count': len(cart),
        'total_price': total_price,
    })
    
def orderlist(request):
    order = Order.objects.all()
    return render(request,'orderlist.html',{'order':order})
    
def suborderdetail(request,pk):
    order = OrderItem.objects.filter(pk=pk)
    print(order)
    return render(request,'suborderdetail.html',{'order':order})
     
