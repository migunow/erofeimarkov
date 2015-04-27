#coding: utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .cart import CartService
from catalog.models import Item


class CartView(View):
    def get(self, request):
        return HttpResponse()

    def post(self, request):
        cs = CartService(request)
        data = request.POST
        if 'cart_item_id' in data:
            cs.change(data['cart_item_id'], data['quantity'], data['size'])
        else:
            product = Item.objects.get(id=data.get('product_id'))
            cs.add(product=product, quantity=data.get('quantity', 1), size=data.get('size'))
        return HttpResponse()

    def delete(self, request, pk):
        cs = CartService(request)
        cs.remove(pk)
        return HttpResponse()


class OrderView(View):
    def get(self, request):
        ctx = {
            'range': range(1, 11),
        }
        return render(request, 'cart/order.html', ctx)
