# coding: utf-8

from .cart import CartService


def cart(request):
    ctx = {
        'cart': CartService(request),
    }
    return ctx



