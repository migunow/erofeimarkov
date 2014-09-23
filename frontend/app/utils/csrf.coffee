"use strict"
$ ->
  getCookie = (name) ->
    cookieValue = null
    if document.cookie and document.cookie isnt ""
      cookies = document.cookie.split(";")
      i = 0
      while i < cookies.length
        cookie = $.trim(cookies[i])
        # Does this cookie string begin with the name we want?
        if cookie.substring(0, name.length + 1) is (name + "=")
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        i++
    cookieValue
  csrfSafeMethod = (method) ->
    # these HTTP methods do not require CSRF protection
    /^(GET|HEAD|OPTIONS|TRACE)$/.test method

  csrftoken = getCookie("csrftoken")
  $.ajaxSetup
    crossDomain: false # obviates need for sameOrigin test
    beforeSend: (xhr, settings) ->
      xhr.setRequestHeader "X-CSRFToken", csrftoken  unless csrfSafeMethod(settings.type)