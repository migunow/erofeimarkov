# coding: utf-8

from django.core.paginator import Paginator
from cart.cart import ItemPriceCalculatorMixin


class CustomPaginator(Paginator):

    pages_count = 8

    pages_half = int(pages_count / 2)

    def __init__(self, *args, **kwargs):
        super(CustomPaginator, self).__init__(*args, **kwargs)
        self.current_page = None

    def make_range(self, x1, x2):
        raw_range = range(x1, x2)
        raw_range = [1] + raw_range + [self.num_pages]
        return sorted(list(set(raw_range)))

    def get_range(self):

        first_page = 1
        last_page = self.num_pages
        current_page = self.current_page

        #все страницы умещаются и так
        if last_page < self.pages_count:
            return self.make_range(first_page, last_page)
        #если текущая страница близка к концу, то обрезаем верх
        if last_page - self.pages_half < current_page:
            return self.make_range(last_page - self.pages_count + 1, last_page + 1)

        #если текущая страница близка к началу, то обрезаем низ
        if current_page < self.pages_half:
            return self.make_range(first_page, first_page + self.pages_count)

        #если мы просто где-то посередине - отступаем с 2х сторон одинаково
        return self.make_range(current_page - self.pages_half, current_page + self.pages_half)


class CustomItem(ItemPriceCalculatorMixin):
    def __init__(self, item, user):
        self.user = user
        self.item = item

    def price(self):
        #если изделия имеет размеры - то считаем по размерам
        if self.item.type.sizes:
            _item = self.item.itemsizes_set.all()
            if _item.exists():
                return self.get_price(_item[0])
            else:
                return self.get_price(self.item)

        #если нет - то просто выдаем цену по каталогу
        else:
            return self.get_price(self.item)

    def price_retail(self):
        #если изделия имеет размеры - то считаем по размерам
        if self.item.type.sizes:
            _item = self.item.itemsizes_set.all()

            # FIXED
            # indexError at /catalog/, если нет ни одного размера для изделия

            if _item.exists():
                return _item[0].price_retail
            else:
                return self.item.price_retail

        #если нет - то просто выдаем цену по каталогу
        else:
            return self.item.price_retail

    def has_sale(self):
        if self.price() != self.price_retail():
            return True
        else:
            return False
