var zoom = 16;


$(window).bind("load", function() {

});


$(document).ready(function() {

//Checkbox custom CSS


 if($('.md-check').length>0){
 $('.md-check').iCheck({
    checkboxClass: 'md-check'
   
  });
 }

 //Featured, Arrival Tab controller
 
 
$('.panel-title > a').click(function(e) {
    e.preventDefault();
    $('.panel-collapse.in').collapse('hide');


    var targetAccordion = $($(this).attr('href'));

    targetAccordion.collapse('show');


});


//PlaceHolders controller for input

$('input,textarea').focus(function() {
    $(this).data('placeholder', $(this).attr('placeholder'))
    $(this).attr('placeholder', '');
});
$('input,textarea').blur(function() {
    $(this).attr('placeholder', $(this).data('placeholder'));
});


//DropDown Menu

  $(".top-menu .dropdown").hover(
            function(){ $(this).addClass('open'); },
            function(){ $(this).removeClass('open'); }
        );


//Top menu select (responsive mode) controller



  $('.top-drop-menu').change(function() {
        var loc = ($(this).find('option:selected').val());
 window.location = loc;
    
    });
    

$('.payment-method-buttons button').click(function(e) {
    e.preventDefault();
    $(this).toggleClass('selected');
});
$('.section-shopping-cart-page .cart-item .close-btn').click(function(event) {
    event.preventDefault();
    el = $(this).parent().parent();
    el.fadeOut(function() {
        el.remove();
    });
});


//    Lightbox activator
    
if($('a[data-rel="prettyphoto"]').length>0){
$('a[data-rel="prettyphoto"]').prettyPhoto();
}





//Color Options background color setters (radio buttons)
    if ($('.color-option').length > 0) {
        $('.color-option').each(function() {

            color = $(this).attr('data-color');
            $(this).css('background-color', color);
        });

    }


//Sidebar widget activator
    if ($('.accordion-widget').length > 0) {
//        $('.category-accordions .accordion-body').parent().find('.accordion-toggle').toggleClass('collapsed');

//        $('.category-accordions .accordion-body').collapse("hide");


        $('.accordion-body').on('hidden', function() {



        });

        $('.accordion-body').on('shown', function() {

        });

    }




//Grid/list buttons switchers on product sidebar page
    if ($('.grid-list-buttons').length > 0) {

        //setTimeout(checkMiniGalleries, 200);
    }

    $('.grid-list-buttons a').click(function(e) {
        e.preventDefault();
        //setTimeout(checkMiniGalleries, 200);

    });



//Brand Slider activator

    


//Image lazy activator
    if ($("img.lazy").length > 0) {
           allImgs = $("img.lazy").length;
        $("img.lazy").each(function(i) {

            src = $(this).attr('src');
            $(this).attr('data-original', src);
 if (i + 1 >= allImgs) {

            $("img.lazy").lazyload({
                effect: "fadeIn"
            });

        }
           

        });



    }
    
    
    
    
//    Footer products image lazy activator
    if ($(".footer-products").length > 0) {
        $(".footer-products img").lazyload({
            effect: "fadeIn"
        });

    }
    
    
//    Tabs controller
    $('.active-tab').click(function(event) {
        event.preventDefault();
    });
    $('#homepage-products-tab .nav-tabs a.tab-control').click(function(event) {
        event.preventDefault();
        parentEl = $(this).parent().parent().parent().parent();
        parentEl.find('.active-tab').text($(this).text());



        $("#homepage-products-tab  .active").removeClass('active');
        $(this).tab('show');
        parentEl.addClass('active');



        if (parentEl.find('.hover-holder li.active').length > 0) {
            parentEl.find('.nav-tabs > li').addClass('active');
        }



        setTimeout(function() {
            checkMiniGalleries();

        }, 200);

    });




   
   

    function clearAnimations() {

        $('.flex-caption .texts-holder:before,.flex-caption .texts-holder:after').animate({
            'opacity': 0
        });
        $('.animated.bounceInUp').each(function() {
            $('.animated.bounceInUp').removeClass('animated').removeClass('bounceInUp');
        });

        $('.animated.bounceOutUp').each(function() {
            $('.animated.bounceOutUp').removeClass('animated').removeClass('bounceOutUp');
        });


        $('.animated.bounceInLeft').each(function() {
            $('.animated.bounceInLeft').removeClass('animated').removeClass('bounceInLeft');
        });


    }
    
    
//    Homepage 1 slider activator
 setupSliderStyle1();
 
 function setupSliderStyle1() {


        if ($('.flexslider').length > 0) {
            $('.flexslider').flexslider({
                prevText: "",
                nextText: "",
                slideshow: true,
                start: function(slider) {
                    $('.flexslider').find('.preloader').removeClass('loading');
                    cs = slider.find('.slide').eq(slider.currentSlide);



                    bl = cs.find('.flex-caption .back-layer');
                    flimg = cs.find('.flex-caption .front-layer .image');
                    fltxt = cs.find('.flex-caption .front-layer .texts-holder');
                    
             
                    bl.find('.anim').addClass('animated bounceInUp');




                    setTimeout(function() {

    

                 flimg.find('.anim').addClass('animated bounceInLeft');

                      




                    }, 500);

                    setTimeout(function() {


                        fltxt.find('.anim').addClass('animated bounceInUp');





                    }, 800);



                    
                },
                after: function(slider) {
                    $('.flexslider').find('.preloader').removeClass('loading');
                    cs = slider.find('.slide').eq(slider.currentSlide);



                    bl = cs.find('.flex-caption .back-layer');
                    flimg = cs.find('.flex-caption .front-layer .image');
                    fltxt = cs.find('.flex-caption .front-layer .texts-holder');

                    bl.find('.anim').addClass('animated bounceInUp');

                    setTimeout(function() {


                        flimg.find('.anim').addClass('animated bounceInLeft');




                    }, 500);

                    setTimeout(function() {


                        fltxt.find('.anim').addClass('animated bounceInUp');




                    }, 800);

                },
                before: function(slider) {
                    $('.flexslider').find('.preloader').addClass('loading');
                    cs = slider.find('.slide').eq(slider.currentSlide);
                    el = cs.find('.flex-caption div');
                    bl = cs.find('.flex-caption .back-layer');
                    fl = cs.find('.flex-caption .front-layer');
                    clearAnimations();
                    fl.find('.anim').addClass('animated bounceOutUp');

                    bl.find('.anim').addClass('animated bounceOutUp');



                }
            });

        }

    }
    
    
//    Top page cart close button
    $('.top-cart-holder .hover-holder .remove-item').click(function(event) {
        event.preventDefault();
        $(this).parent().parent().fadeOut(function() {
            $(this).remove();
        });
    });



//Contact form setup

    checkContactForm();
    function checkContactForm() {
        if ($(".contact-form").length > 0) {


            //  triggers contact form validation
            var formStatus = $(".contact-form").validate();
            //   ===================================================== 
            //sending contact form
            $(".contact-form").submit(function(e) {
                e.preventDefault();

                if (formStatus.errorList.length === 0)
                {
                    $(".contact-form .submit").fadeOut(function() {
                        $('#loading').css('visibility', 'visible');
                        $.post('submit.php', $(".contact-form").serialize(),
                                function(data) {
                                    $(".contact-form input,.contact-form textarea").not('.submit').val('');

                                    $('.message-box').html(data);


                                    $('#loading').css('visibility', 'hidden');
                                    $(".contact-form .submit").removeClass('disabled').css('display', 'block');
                                }

                        );
                    });


                }

            });
        }
    }
});