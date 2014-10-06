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

check_available_size()

$('#js-sizes').change (event)->
  console.log 'change_size'
  check_available_size()
