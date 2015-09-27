#coding: utf-8
import logging

from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

from cart.cart import CartService, CART_ID
from notifications.notifier import send_notification
from notifications.smssend import sendsms
from order.models import Order

logger = logging.getLogger(__name__)

class OrderView(View):
    def get(self, request):
        return render(request, 'cart/after_order.html')

    def post(self, request):
        order = Order()
        order.cart_id = request.session.get(CART_ID)
        order.address = request.POST.get('address')
        order.phone = request.POST.get('phone')
        order.name = request.POST.get('name')
        order.processed = False
        order.comment = request.POST.get('comment')
        if request.user.is_authenticated():
            order.customer = request.user
        order.save()

        cart = CartService(request)
        cart.checkout()

        params = {
            "phone": unicode(request.POST.get('phone')),
            "customer": request.user,
            "comment": order.comment,
            "orderno": order.id,
            "orderdt": order.checkout_date,
            "ordercart": cart,
        }

        send_notification("order_notice", params)

        return render(request, 'cart/after_order.html')
