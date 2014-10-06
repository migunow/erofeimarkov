#coding: utf-8

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Min, Max
from django.shortcuts import render
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

    def get_price_range(self, request):
        price_column = self.get_user_price_field(request)
        return Item.objects.all().aggregate(price_min=Min(price_column), price_max=Max(price_column))

    def get(self, request):
        #создаем переданные фильтры
        filters = {}
        new = int(request.GET.get('new', 0))
        if new == 1:
            new = True
            filters['new'] = True
        else:
            new = False
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

        #фильтруем по цене
        wide_price = self.get_price_range(request)
        if 'price_min' in request.GET:
            price_filter = {
                'price_min': int(request.GET.get('price_min')),
                'price_max': int(request.GET.get('price_max')),
            }
            filters['{}__gte'.format(self.get_user_price_field(request))] = price_filter['price_min']
            filters['{}__lte'.format(self.get_user_price_field(request))] = price_filter['price_max']
        else:
            price_filter = wide_price

        #поиск по артикулу
        article_key = request.GET.get('search', '')
        if article_key:
            filters['article__icontains'] = article_key

        query_set = Item.objects.filter(**filters)
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

        #вид сетка или список
        catalog_view = request.GET.get('view')
        if catalog_view:
            view_list = True
        else:
            view_list = False

        ctx = {
            'item_categories': ItemCategory.objects.all(),
            'item_types': ItemType.objects.all(),
            'insertion_kinds': InsertionKind.objects.all(),
            'filter_categories': filter_categories,
            'filter_insertions': filter_insertions,
            'filter_types': filter_types,
            'new': new,
            'products': custom_items,
            'paginator': paginator,
            'cart_positions': cart_positions,
            'prices': wide_price,
            'price_filter': price_filter,
            'ordering_filter': ordering_filter,
            'view_list': view_list,
            'search_text': article_key,
        }

        return render(request, 'catalog/catalog.html', ctx)


class ItemView(View):
    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        all_sizes = item.type.get_sizes()
        
        available_sizes = dict ((itemsize.size, CustomItemSize(itemsize, request.user)) for itemsize in item.itemsizes_set.all())
        
        sizes = []
        marked = False
        for size in all_sizes:
            raw_size = {
                "size" : size,
                "selected" : not marked and size in available_sizes,
                "available" : size in available_sizes,
                "price" : available_sizes[size].get_price(available_sizes[size].item) if size in available_sizes else False,
                "retailprice" : available_sizes[size].item.price_retail if size in available_sizes else False
            }
            if (raw_size["selected"]):
                marked = True
            print raw_size
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
