console.log 'menu_highlight'

location = window.location.pathname

mark = (el_category)->
#  $(".js-menu[data-category=#{el_category}]").css('font-size', 'x-large')

switch location
  when '/catalog/' then mark('catalog')
  when '/delivery/' then mark('delivery')
  when '/about/' then mark('about')
  when '/blog/' then mark('blog')
  when '/authentication/login/' then mark('login')
