#coding: utf-8
import logging
import json
from datetime import datetime

from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import View

from cart.cart import CartService, CART_ID
from cart.models import Cart, Item
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
            "name": None,
            "customer": request.user,
            "comment": order.comment,
            "orderno": order.id,
            "orderdt": order.checkout_date,
            "orderaddr": order.address,
            "ordercart": cart,
        }

        send_notification("order_notice", params)

        return render(request, 'cart/after_order.html')

class QuickOrder(View):
    def post(self, request):
        cart = Cart()
        cart.save()
        item = Item()
        item.cart = cart
        item.quantity = int(request.POST.get("quantity", 1))
        item.product_id = int(request.POST["product_id"])
        item.save()

        order = Order()
        order.cart_id = cart.id
        order.address = "Уточнить у клиента"
        order.phone = request.POST.get('phone')
        order.name = request.POST.get('name')
        order.comment = "Заказ в один клик"
        if request.user.is_authenticated():
            order.customer = request.user
        order.save()

        cart_service = CartService(request, cart)

        params = {
            "phone": unicode(request.POST["phone"]),
            "name": unicode(request.POST["name"]),
            "customer": request.user,
            "comment": order.comment,
            "orderno": order.id,
            "orderdt": order.checkout_date,
            "orderaddr": order.address,
            "ordercart": cart_service,
        }

        send_notification("order_notice", params)
        response = HttpResponse(json.dumps({"order_id": order.id, "ok": 1}),
                                content_type="application/json")
        return response


class CallMeBack(View):
    def post(self, request):
        user = request.user
        if user.is_authenticated():
            role = 'Авторизированный пользователь {}'.format(user.id)
            if user.role == user.ROLE_WHOLESALER:
                role = 'Наш оптовик {}'.format(user.id)
        else:
            role = 'Навторизированный пользователь'

        params = {
            "phone": unicode(request.POST["phone"]),
            "name": unicode(request.POST["name"]),
            "user_role": role,
            "dt": datetime.now()
        }
        try:
            send_notification("callme_back", params)
        except Exception as e:
            logger.error("Cannot send callme_back notification: %s" % str(e))
            return HttpResponse(json.dumps({"ok": 0}),
                                content_type="application/json")

        response = HttpResponse(json.dumps({"ok": 1}),
                                content_type="application/json")
        return response
