#coding: utf-8
from django.shortcuts import render
from django.views.generic import View
from cart.cart import CartService, CART_ID
from order.models import Order
from notifications.models import *
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from notifications.smssend import sendsms


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

        emails = list(EmailContact.objects.all().values_list('email', flat=True))
        if emails:
            html_content = render_to_string('email_templates/ordernotice.html', {
                "customer": request.user,
                "comment": order.comment,
                "orderno": order.id,
                "orderdt": order.checkout_date,
                "ordercart": cart,
            })

            msg = EmailMessage()
            msg.subject = u"Поступил новый заказ от пользователя " + unicode(request.POST.get('phone'))
            msg.body = html_content
            msg.from_email = 'Erofeimarkov.ru <noreply@erofeimarkov.ru>'
            msg.to = emails
            msg.content_subtype = "html"
            sent_count = msg.send()

        phones = ','.join(SMSContact.objects.all().values_list('phoneno', flat=True))
        if phones:
            try:
                message = u'Поступил заказ #' + unicode(order.id) + u' от пользователя '+ unicode(request.POST.get('phone'))
                sendsms(phones, message)
            except:
               print('Could not send sms')
        return render(request, 'cart/after_order.html')
