from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
import json
import datetime
from .models import * 
from .utils import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,auth

def orders(request):
	order_items = OrderItem.objects.all()
	order = Order.objects.all()
	return render(request, 'store/orders.html', {'order_items': order_items,'order': order})


def delete(request, pk):
	data = Product.objects.get(pk=pk) 
	data.delete()
	return redirect('inventory')

def update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Handle form submission here
        type = request.POST.get('type')
        product_name = request.POST.get('product')
        price = request.POST.get('price')
        quantity = request.POST.get('qty')
        new_photo = request.FILES.get('photo')

        # Update the product's fields
        product.type = type
        product.product = product_name
        product.price = price
        product.qty = quantity

        if new_photo:
            product.photo = new_photo

        product.save()
        return redirect('inventory')

    return render(request, 'store/update.html', {'product': product})

def toggle_item(request, pk):
    item = Product.objects.get(pk=pk)
    item.is_enabled = not item.is_enabled
    item.save()
    return redirect('inventory')

def logoutuser(request):
	logout(request)
	return redirect('login')

def inventory(request):
	inventory_items = Product.objects.all()
	product_count = Product.objects.all().count()
	order_count = Order.objects.all().count()
	context = {'inventory_items': inventory_items,'product_count': product_count, 'order_count':order_count}
	return render(request,'store/inventory.html',context)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('inventory')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')


    return render(request, 'store/login.html')

from .models import User, Customer  # Import your custom User and Customer models

def registration(request):
	if request.method == 'POST':
		store_number=request.POST.get('store_number')
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		username = request.POST.get('username')
		store_name = request.POST.get('store_name')
		password= request.POST.get('password')
		email = request.POST.get('email')
		if User.objects.filter(username=username).exists():
			messages.error(request, "Username is taken.")
		else:
			user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password,
                store_name=store_name,
				store_number=store_number,
            )
			customer = Customer(user=user, name=f"{first_name} {last_name}", email=email)
			customer.save()
			messages.success(request, "Account created successfully. You are now logged in.")
			return redirect('login')  # Redirect to a suitable view
	return render(request, 'store/registration.html')



def add(request):
	if request.method == 'POST':
		type = request.POST.get('type')
		price = request.POST.get('price')
		name = request.POST.get('name')
		image = request.FILES.get('image')
		store_name = request.POST.get('store_name')
		store_number= request.POST.get('store_number')
		drink =Product.objects.create( price=price, name=name, image=image , type=type, store_name=store_name , store_number=store_number)
		drink.save()
		return redirect('inventory')
	return render(request, 'store/add.html')

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def store2(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store2.html', context)


def store3(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store3.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

# cart2

def cart2(request):
	data = cartData2(request)

	cartItems2 = data['cartItems2']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems2':cartItems2}
	return render(request, 'store/cart2.html', context)

def checkout2(request):
	data = cartData2(request)
	
	cartItems2 = data['cartItems2']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems2':cartItems2}
	return render(request, 'store/checkout2.html', context)

def updateItem2(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)