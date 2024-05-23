from django.shortcuts import render

from django.http import JsonResponse

import json

from .models import *

from django.contrib.auth.decorators import login_required

import datetime


from .utils import cookieCart

# Create your views here.


def store(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

	


def cart(request):
	
	if request.user.is_authenticated:

		print('Fucking i am authenticated')
		
		customer = request.user.customer

		order, created = Order.objects.get_or_create(customer=customer, complete=False)

		print('Orders : ', order)
	
		items = order.orderitem_set.all()

		print('Items Ordered : ', items)

		cartItems = order.get_cart_items

	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']


	# print('Request : ' ,request)
	# print('Request User : ' ,request.user)
	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order = Order.objects.get(customer=customer)
	# 	print('Order object : ', order)
	# 	order_id = order.id
	# 	print('Order Id: ', order_id)
	# 	# items = OrderItem.objects.filter(order=order_id)
	# 	items = order.orderitem_set.all()
	# 	print('Ordered Items : ', items)
	# else:
	# 	#Create empty cart for now for non-logged in user
	# 	items = []
	# 	order = {'get_cart_total':0, 'get_cart_items':0}

	products = Product.objects.all()

	context = {'items':items, 'order':order , 'cartItems':cartItems}

	return render(request, 'store/cart.html', context)





def checkout(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		# order = Order.objects.get(id=1)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()

		cartItems = order.get_cart_items

	else:
		cookieData = cookieCart(request)
		cartItems = cookieData['cartItems']
		order = cookieData['order']
		items = cookieData['items']

	context = {'items':items, 'order':order , 'cartItems':cartItems}
	

	return render(request, 'store/checkout.html', context)

	


def updateItem(request):
	data = 	json.loads(request.body)

	productId = data['productId']
	action = data['action']

	print('Action:',action)
	print('productId:',productId)

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
	else:
		print('User is not logged in')

	return JsonResponse('Payment submitted..', safe=False)

