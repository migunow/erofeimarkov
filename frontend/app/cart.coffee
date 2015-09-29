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

$confirmDialog = $("#oneclick-order-confirmation")
$confirmDialog.dialog
  autoOpen: false
  title: "Спасибо. Ваш заказ принят в обработку"
  hide: "fade"
  modal: true
  dialogClass: "dialog-no-close"
  width: 500
  resizable: false
  dragable: false

$confirmDialog.on("click", () -> $confirmDialog.dialog("close"))

$dialog = $('#oneclick-order-dialog')
$dialog.find("input.js-phone").inputmask('+7(999)-999-99-99')
$dialog.find("button.md-button.large").on("click", (event) ->
  event.preventDefault()
  data =
    'product_id': $('input[name="product_id"]').val()
    'name': $('input[name="name"]').val()
    'phone': $('input[name="phone"]').val()
  url = "/order/quick_order/"
  $.post(url, data, (response)->
    order_id = response.order_id
    $confirmDialog = $("#oneclick-order-confirmation")
    #$confirmDialog.find("#oneclick-order-id").text(order_id)
    $confirmDialog.dialog("open")
    closeFunc = ()-> $confirmDialog.dialog("close")
    timeout = setTimeout(closeFunc, 5000)
    $confirmDialog.on("close", ()-> clearTimeout(timeout))
  )
  $dialog.dialog("close")
)
$dialog.dialog
  autoOpen: false
  title: "Быстрый заказ"
  hide: "fade"
  modal: true
  resizable: false
  dragable: false



$(".js-buy-one-click").on("click", (event) ->
  event.preventDefault()
  $el = $(event.currentTarget)
  item_id = $el.data("id")
  $dialog = $('#oneclick-order-dialog')
  $dialog.find('input[name="product_id"]').val(item_id)
  $dialog.dialog("open")
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
