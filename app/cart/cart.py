#coding: utf-8
from __future__ import unicode_literals

from .models import Cart, Item

CART_ID = 'cart_id'


class ItemPriceCalculatorMixin(object):

    def get_price(self, obj):
        if self.user.is_authenticated():
            price = obj.price_wholesale
            if self.user.role == self.user.ROLE_WHOLESALER:
                price = obj.price_primary_wholesale
        else:
            price = obj.price_retail
        return price


class CartItemService(ItemPriceCalculatorMixin):
    def __init__(self, user, cart_item):
        self.user = user
        self.cart_item = cart_item

    def price(self):
        if self.cart_item.product.special_price:
            return self.cart_item.product.special_price
        else:
            #если изделия имеет размеры - то считаем по размерам
            if self.cart_item.product.type.sizes:
                _item = self.cart_item.product.itemsizes_set.get(size=self.cart_item.size)
                return self.get_price(_item)
            #если нет - то просто выдаем цену по каталогу
            else:
                return self.get_price(self.cart_item.product)


    def total(self):
        return self.cart_item.quantity * self.price()

    def get_full_name(self):
        if not self.cart_item.product.type.sizes:
            return self.cart_item.product.get_full_name()
        else:
            return '{} #{}'.format(self.cart_item.product.get_full_name(), self.cart_item.size)


class CartService(object):
    def __init__(self, request):
        self.user = request.user
        cart_id = request.session.get(CART_ID)
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id, checked_out=False)
            except Cart.DoesNotExist:
                cart = self.new(request)
        else:
            cart = self.new(request)
        self.cart = cart

    def __iter__(self):
        for item in self.cart.item_set.all():
            yield CartItemService(self.user, item)

    def is_empty(self):
        if len(self.cart.item_set.all()) > 0:
            return True
        else:
            return False

    def new(self, request):
        cart = Cart()
        cart.save()
        request.session[CART_ID] = cart.id
        return cart

    def add(self, product, quantity=1, size=None):
        if not size and product.type.sizes:
            size = product.itemsizes_set.all()[0].size
        else:
            size = size
        try:
            item = Item.objects.get(
                cart=self.cart.id,
                product=product,
                size=size
            )
        except Item.DoesNotExist:
            item = Item()
            item.cart = self.cart
            item.product = product
            item.quantity = quantity
            item.size = size
            item.save()
        item.quantity = int(quantity)
        item.size = size
        item.save()
        return item

    def change(self, cart_item_id, quantity, size):
        cart_item = Item.objects.get(id=cart_item_id)
        cart_item.quantity = int(quantity)
        cart_item.size = size
        cart_item.save()

    def remove(self, item_id):
        try:
            item = Item.objects.get(
                cart=self.cart,
                id=item_id,
            )
        except Item.DoesNotExist:
            pass
        else:
            item.delete()

    def count(self):
        return len(self.cart.item_set.all())

    def total(self):
        return sum([item.price() * item.cart_item.quantity for item in self])

    def clear(self):
        for item in self.cart.item_set.all():
            item.delete()

    def checkout(self):
        self.cart.checked_out = True
        self.cart.save()

    def get_user_role(self):
        if self.user.is_authenticated():
            role = 'Авторизированный пользователь {}'.format(self.user.id)
            if self.user.role == self.user.ROLE_WHOLESALER:
                role = 'Наш оптовик {}'.format(self.user.id)
        else:
            role = 'Навторизированный пользователь'
        return role


