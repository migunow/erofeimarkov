console.log 'order'


change_cart_item =  (event)=>
  $el = $(event.currentTarget)
  url = '/cart/add/'
  data =
    cart_item_id: $el.closest('.cart-item').data('id')
    quantity: $el.closest('.cart-item').find('.js-change-quantity').find('option:selected').val()
    size: $el.closest('.cart-item').find('.js-change-size').find('option:selected').val()
  $.post(url, data, (response)=>
    window.location.reload()
  )

$('.js-change-quantity').on 'change', change_cart_item
$('.js-change-size').on 'change', change_cart_item
