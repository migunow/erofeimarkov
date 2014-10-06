check_available_size = ->
  size_selectbox = $('#js-sizes')
  availability_container = $("#js-availability-container")

  availability_container.removeClass('available').removeClass('not-available').removeClass('no-size-available')

  has_sizes = !!size_selectbox.length

  if has_sizes
    if size_selectbox.find('option:selected').data('available') && availability_container.data('available-balance')
      availability_container.addClass('available')
    else
      availability_container.addClass('no-size-available')
  else
    if availability_container.data('available-balance')
      availability_container.addClass('available')
    else
      availability_container.addClass('not-available')

update_price = ->
  size_selectbox = $('#js-sizes')
  if !!size_selectbox.length
    price_container = $('#js-price')
    selected = size_selectbox.find('option:selected')
    price = selected.data('price')||price_container.data('price')
    retailprice = selected.data('retailprice')||price_container.data('retailprice')
    price_container.children('.current-price').text(price + ' руб.')
    if !retailprice || price == retailprice
      price_container.children('.previous-price').hide()
    else
      price_container.children('.previous-price').text(retailprice + ' руб.').show()


check_available_size()
update_price()

$('#js-sizes').change (event)->
  console.log 'change_size'
  check_available_size()
  update_price()
