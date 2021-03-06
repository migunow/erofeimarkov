#coding: utf-8

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from cart.cart import CART_ID, ItemPriceCalculatorMixin
from catalog.utils import CustomPaginator, CustomItem, CustomItemSize

from .models import ItemCategory, ItemType, InsertionKind, Item


class CatalogView(View):

    per_page = 15

    def convert(self, param):
        if param:
            return [int(x) for x in param[1:-1].split(',')]
        else:
            return tuple()

    def get_user_price_field(self, request):
        if request.user.is_authenticated():
            price_column = 'price_wholesale'
            if request.user.role == request.user.ROLE_WHOLESALER:
                price_column = 'price_primary_wholesale'
        else:
            price_column = 'price_retail'

        return price_column

    def get(self, request):
        #создаем переданные фильтры
        filters = {}
        new = int(request.GET.get('new', 0))
        if new == 1:
            new = True
            filters['new'] = True
        else:
            new = False

        special = int(request.GET.get('special', 0))
        if special == 1:
            special = True
            filters['special'] = True
        else:
            special = False

        instock = int(request.GET.get('instock', 0))
        if instock == 1:
            filters['balance__gt'] = 0;

        filter_categories = self.convert(request.GET.get('categories'))
        if filter_categories:
            filters['category__id__in'] = filter_categories

        filter_insertions = self.convert(request.GET.get('insertions'))
        if filter_insertions:
            filters['iteminsertions__kind__id__in'] = filter_insertions

        filter_types = self.convert(request.GET.get('types'))
        if filter_types:
            filters['type__id__in'] = filter_types

        #сортируем по цене
        ordering_filter = ''
        ordering = request.GET.get('order_by')
        if ordering:
            if ordering == 'price':
                ordering = self.get_user_price_field(request)
                ordering_filter = '+'
            elif ordering == '-price':
                ordering = '-' + self.get_user_price_field(request)
                ordering_filter = '-'
            else:
                ordering = None

        #поиск по артикулу
        article_key = request.GET.get('search', '')
        if article_key:
            filters['article__icontains'] = article_key

        query_set = Item.objects.select_related('type', 'category').filter(is_deleted=False, **filters).prefetch_related("itemsizes_set").distinct()
        if ordering:
            query_set = query_set.order_by(ordering)

        #паджинация
        paginator = CustomPaginator(query_set, self.per_page)

        page = request.GET.get('page')
        try:
            items = paginator.page(page)
            paginator.current_page = int(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            items = paginator.page(1)
            paginator.current_page = 1
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            items = paginator.page(paginator.num_pages)
            paginator.current_page = paginator.num_pages

        custom_items = [CustomItem(item, request.user) for item in items]

        #позиции в корзине
        cart_id = request.session.get(CART_ID)
        if cart_id:
            cart_positions = Item.objects.filter(item__cart=cart_id).values_list('id', flat=True)
        else:
            cart_positions = []

        ctx = {
            'item_categories': ItemCategory.objects.all(),
            'item_types': ItemType.objects.all(),
            'insertion_kinds': InsertionKind.objects.all(),
            'filter_categories': filter_categories,
            'filter_insertions': filter_insertions,
            'filter_types': filter_types,
            'new': new,
            'instock': instock,
            'special': special,
            'products': custom_items,
            'paginator': paginator,
            'cart_positions': cart_positions,
            'ordering_filter': ordering_filter,
            'search_text': article_key,
        }

        return render(request, 'catalog/catalog.html', ctx)


class ItemView(View):
    def get(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id, is_deleted=False)

        all_sizes = item.type.get_sizes()
        available_sizes = dict ((itemsize.size, CustomItemSize(itemsize, request.user)) for itemsize in item.itemsizes_set.all())

        rsize = request.GET.get("size", None)
        if rsize is not None and rsize not in all_sizes:
            rsize = None

        sizes = []
        marked = False

        for size in all_sizes:
            selected = False
            if not marked:
                if rsize is not None:
                    selected = (rsize == size)
                else:
                    selected = size in available_sizes
            if not item.special:
                price = available_sizes[size].get_price(available_sizes[size].item) if size in available_sizes else False
            else:
                price = item.special_price

            raw_size = {
                "size" : size,
                "selected" : selected,
                "available" : size in available_sizes,
                "price" : price,
                "retailprice" : available_sizes[size].item.price_retail if size in available_sizes else False
            }
            if selected:
                marked = True
            sizes.append(raw_size)

        #позиции в корзине
        cart_id = request.session.get(CART_ID)
        cart_positions = Item.objects.filter(item__cart=cart_id).values_list('id', flat=True)
        ctx = {
            'product': CustomItem(item, request.user),
            'sizes': sizes,
            'cart_positions': cart_positions,
        }
        return render(request, 'catalog/item.html', ctx)
