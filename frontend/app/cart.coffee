console.log('cart')
$('.js-add-to-cart').on('click', (event)->
  event.preventDefault()
  $el = $(event.currentTarget)
  url = '/cart/add/'
  data =
    'product_id': $el.data('id')
    'size': $('#js-sizes').find('option:selected').val()
    'quantity': $('#js-quantity').find('option:selected').val()
    'comment': $('#js-comment').val()
  $.post(url, data, (response)=>
    window.location.reload()
  )
)


$('.js-delete-from-cart').on('click', (event)->
  event.preventDefault()
  $el = $(event.currentTarget)
  item_id = $el.data('id')
  $.ajax
    url: "/cart/delete/#{item_id}/"
    type: 'delete'
    success: (response) =>
      window.location.reload()
)

$('#js-phone').inputmask('+7(999)-999-99-99')

make_search = (event)->
  event.preventDefault()
  text = $('#js-search-from-cart').val()
  new_url = "/catalog/?search=#{text}"
  window.location.href = new_url

#поиск из меню корзины
$('#js-search-from-cart').on
  change: make_search

$('#js-search-from-cart-submit').on
  submit: make_search