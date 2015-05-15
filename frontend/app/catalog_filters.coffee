console.log 'catalog_filters'

class Filter

  category_filters: []

  insertion_filters: []

  type_filters: []

  new_filter: false

  instock_filter: false

  special_filter: false

  sorting: ''

  price_filter: ''

  page: undefined

  view: 'grid-view'

  trigger_filter: (event)=>
    $el = $(event.currentTarget)
    $el.toggleClass('category-selected')
    @prepare_query_string()

  trigger_sort: (event)=>
    $el = $(event.currentTarget)
    $('.js-sorting-order').removeClass('category-selected')
    $el.addClass('category-selected')
    @prepare_query_string()

  trigger_page: (event)=>
    $el = $(event.currentTarget)
    $('.js-page').removeClass('js-active')
    $el.addClass('js-active')
    @prepare_query_string()

  make_query_str: (name, ids)=>
    unless ids.length==0
      _ids = ids.join(',')
      return "#{name}=[#{_ids}]"
    else
      return ''

  prepare_query_string: =>
    #сортировка
    sorting = $('.js-sorting-order.category-selected').data('sorting')
    if sorting != undefined
      sorting = "order_by=#{sorting }"
    else
      sorting = ''
    #паджинация
    page_number = $('.js-page.js-active').data('page')
    if page != '1'
      page = "page=#{page_number}"
    else
      page = ''

    #категории
    @new_filter = $('#js-new-filter').hasClass('category-selected')
    if @new_filter
      new_filter = "new=1"
    else
      new_filter = ''

    @instock_filter = $('#js-instock-filter').hasClass('category-selected')
    if @instock_filter
      instock_filter = "instock=1"
    else
      instock_filter = ''

    #категории
    @special_filter = $('#js-special-filter').hasClass('category-selected')
    if @special_filter
      special_filter = "special=1"
    else
      special_filter = ''

    @search_string = $('#js-search-from-cart').val()

    if @search_string
      search_string = "search="+@search_string
    else
      search_string = ''


    category_filters = $.map($('#js-category-filter').find('.category-selected'), (value, key)=>return $(value).data('id'))
    insertion_filters = $.map($('#js-insertion-filter').find('.category-selected'), (value, key)=>return $(value).data('id'))
    type_filters = $.map($('#js-type-filter').find('.category-selected'), (value, key)=>return $(value).data('id'))

    categories = @make_query_str('categories', category_filters)
    insertions = @make_query_str('insertions', insertion_filters)
    types = @make_query_str('types', type_filters)
    query_items = [new_filter, instock_filter, special_filter, categories, insertions, types, sorting, page, search_string]
    query_items = query_items.filter((item) ->
      item isnt ""
    )

    query = '?' + query_items.join('&')
    if query == '?'
      query = ''

    redirect_url = window.location.pathname + query
    window.location.replace redirect_url


filter = new Filter()

$('.js-category').on('click', filter.trigger_filter)
$('.js-sorting-order').on('click', filter.trigger_sort)
$('.js-page').on('click', filter.trigger_page)


#Sidebar Price Slider
if $(".price-slider").length > 0
  $el = $('#js-price-filter')
  min_price = +$el.data('price-min')
  max_price = +$el.data('price-max')
  step = Math.round((max_price - min_price) / 70)
  $(".price-slider").slider
    min: min_price
    max: max_price
    step: step
    value: [
      +$el.data('price-min-set')
      +$el.data('price-max-set')
    ]
    handle: "square"
  .on 'slideStop', (event)->
    filter.prepare_query_string()
    console.log 'js-price-filter changed'


$('.js-set-active-tab').click (event)->
  $el = $(event.currentTarget)
  filter.view = $el.data 'id'
  console.log filter.view

