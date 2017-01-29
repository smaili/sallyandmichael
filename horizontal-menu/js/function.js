/*Scripts starts*/
$(document).on('ready', function () {
    'use strict';
    //Vertical icon-menu active script
    $('.horizontal_iconmenu li').on('click', function () {
        $('.page-top').removeClass('display_none');
        $('.wow').attr('style', 'visibility: hidden; animation-name: none; -webkit-transform:translateY(20px); -moz-transform:translateY(20px); -ms-transform:translateY(20px); -o-transform:translateY(20px); transform:translateY(20px); -webkit-animation-duration: 2s; -moz-animation-duration: 2s; -ms-animation-duration: 2s; -o-animation-duration: 2s; animation-duration: 2s;');

        $('.horizontal_iconmenu li').removeClass('hover_active');
        $(this).addClass('hover_active');
        setTimeout(function () {
            $('.wow').each(function () {

                $(this).attr('style', 'visibility: visible; animation-name: ' + $(this).attr('data-class') + '; -webkit-transform:translateY(0px); -moz-transform:translateY(0px); -ms-transform:translateY(0px); -o-transform:translateY(0px); transform:translateY(0px); -webkit-animation-duration: 2s; -moz-animation-duration: 2s; -ms-animation-duration: 2s; -o-animation-duration: 2s; animation-duration: 2s;');
            });
        }, 500);
    });

    $('.other-menu').on('mouseenter', function () {
        $('.hover-menu').animate({ '-moz-transform': 'translate3d(0, 84px, 0px)', '-webkit-transform': 'translate3d(0, 84px, 0px)', '-ms-transform': 'translate3d(0, 84px, 0px)', '-o-transform': 'translate3d(0, 84px, 0px)', 'transform': 'translate3d(0, 84px, 0px)' }, 'fast');
        setTimeout(function () {
            $('.hover-menu').css('-moz-transform', 'translate3d(0, 0px, 0px)').css('-webkit-transform', 'translate3d(0, 84px, 0px)').css('-ms-transform', 'translate3d(0, 84px, 0px)').css('-o-transform', 'translate3d(0, 84px, 0px)').css('transform', 'translate3d(0, 84px, 0px)');
        }, 200);
    });

    $('.other-menu').on('mouseenter', function () {
        $('.hover-menu').animate({ '-moz-transform': 'translate3d(0px, 0px, 0px)', '-webkit-transform': 'translate3d(0px, 0px, 0px)', '-ms-transform': 'translate3d(0px, 0px, 0px)', '-o-transform': 'translate3d(0px, 0px, 0px)', 'transform': 'translate3d(0px, 0px, 0px)', }, 'fast');
        $('.other-menu').addClass('hover_active');
        $('.other-menu a').addClass('hover_active selected');
        setTimeout(function () {
            $('.hover-menu').css('-moz-transform', 'translate3d(0px, 0px, 0px)').css('-webkit-transform', 'translate3d(0px, 0px, 0px)').css('-ms-transform', 'translate3d(0px, 0px, 0px)').css('-o-transform', 'translate3d(0px, 0px, 0px)').css('transform', 'translate3d(0px, 0px, 0px)');
        }, 200);


    }).on('mouseleave', function () {

        $('.hover-menu').animate({ '-moz-transform': 'translate3d(0px, -400px, 0px)', '-webkit-transform': 'translate3d(0px, -400px, 0px)', '-ms-transform': 'translate3d(0px, -400px, 0px)', '-o-transform': 'translate3d(0px, -400px, 0px)', 'transform': 'translate3d(0px, -400px, 0px)' }, 'fast');
        $('.other-menu').removeClass('hover_active');
        $('.other-menu a').removeClass('hover_active selected');
        setTimeout(function () {
            $('.hover-menu').css('-moz-transform', 'translate3d(0px, -400px, 0px)').css('-webkit-transform', 'translate3d(0px, -400px, 0px)').css('-ms-transform', 'translate3d(0px, -400px, 0px)').css('-o-transform', 'translate3d(0px, -400px, 0px)').css('transform', 'translate3d(0px, -400px, 0px)');
        }, 200);
    });

    // JavaScript Document
    var today = new Date();

    var target = new Date(today);
    target.setDate(110); // Set no. of days from today
    target.setHours(0, 0, 0, 0);

    // Countdown start from yesterday
    var yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1); // Day counter will start from yesteday
    yesterday.setHours(0, 0, 0, 0);
    if ($.find('.countdown').length) {
        $('.countdown').final_countdown({
            'start': yesterday.getTime() / 1000,
            'end': target.getTime() / 1000,
            'now': today.getTime() / 1000
        }, function () {
            // Finish Callback
        });
    }
    $(window).load(function () {
        if ($.find('.gridlayout').length) {
            $('.gridlayout').isotope({
                // options...
                itemSelector: '.grid-item',
                masonry: {
                    columnWidth: '.grid-item'
                }
            });
        }
    });


    /*Timer for wedding page*/
    if ($.find('#example').length) {
        $('#example').countdown({
            date: '11/17/2016 23:59:59',
            offset: 0,
            day: 'Day',
            days: 'Days'
        }, function () {

        });
    }
    $('.hamburger').on('click', function () {
        if ($('.navbar-fixed-top').css('right') == '-100px') {
            $('.navbar-fixed-top').animate({ right: '0px' }, 'slow');
        }
        else {
            if ($('.navbar-fixed-top').css('overflow-y') == 'scroll') {
                $('.navbar-fixed-top').animate({ right: '-100px' }, 'slow');
            }
        }
    });
    $('body').on('click', function (evt) {
        if ($('.navbar-fixed-top').css('z-index') == 10030) {
            if (evt.target.class == 'hamburger') {
                return;
            }
            if ($(evt.target).closest('.hamburger').length)
            { return; }
            else
            {
                if ($('.navbar-fixed-top').css('overflow-y') == 'scroll') {
                    $('.navbar-fixed-top').animate({ right: '-100px' }, 'slow');
                }
            }
        }
    });

    //Horizontal Tab
    if ($.find('#parentHorizontalTab').length) {
        $('#parentHorizontalTab').easyResponsiveTabs({
            type: 'default', //Types: default, vertical, accordion
            width: 'auto', //auto or any width like 600px
            fit: true, // 100% fit in a container
            tabidentify: 'hor_1', // The tab groups identifier
            activate: function (event) { // Callback function if tab is switched
                var $tab = $(this);
                var $info = $('#nested-tabInfo');
                var $name = $('span', $info);
                $name.text($tab.text());
                $info.show();
            }
        });
    }
    // Child Tab

    if ($.find('#ChildVerticalTab_1').length) {
        $('#ChildVerticalTab_1').easyResponsiveTabs({
            type: 'vertical',
            width: 'auto',
            fit: true,
            tabidentify: 'ver_1', // The tab groups identifier
            activetab_bg: null,
            inactive_bg: null,
            active_border_color: null,
            active_content_border_color: null
        });
    }
    //Vertical Tab


    if ($.find('#parentVerticalTab').length) {
        $('#parentVerticalTab').easyResponsiveTabs({
            type: 'vertical', //Types: default, vertical, accordion
            width: 'auto', //auto or any width like 600px
            fit: true, // 100% fit in a container
            closed: 'accordion', // Start closed if in accordion view
            tabidentify: 'hor_1', // The tab groups identifier
            activate: function (event) { // Callback function if tab is switched
                var $tab = $(this);
                var $info = $('#nested-tabInfo2');
                var $name = $('span', $info);
                $name.text($tab.text());
                $info.show();
            }
        });
    }

    /*---------------------*/


    /*------------slick slider-------------------*/



    /*-----photo gallery------------*/

    if ($.find('.fancybox').length) {
        $('.fancybox').fancybox();
    }
    //gallery option 2 

    if ($.find('.fancybox2').length) {
        $('.fancybox2').fancybox();
    }
    /*-----------------------------------people page slider------------------------*/

    $('.the-people-slider').slick({
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: true,
        dots: false,
        autoplay: true,
        responsive: [
  {
      breakpoint: 981,
      settings: {
          slidesToShow: 1,
          slidesToScroll: 1,
          arrows: false
      }
  },

   {
       breakpoint: 769,
       settings: {
           slidesToShow: 1,
           slidesToScroll: 1,
           arrows: false
       }
   },
    {
        breakpoint: 640,
        settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false
        }
    },
   {
       breakpoint: 361,
       settings: {
           slidesToShow: 1,
           slidesToScroll: 1,
           arrows: false
       }
   }
   // You can unslick at a given breakpoint now by adding:
   // settings: 'unslick'
   // instead of a settings object
        ]
    });

    $('.ceremony-slider').slick({
        dots: false,
        infinite: true,
        speed: 300,
        autoplay: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        arrows: false,
        responsive: [
          {
              breakpoint: 1025,
              settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                  infinite: true,
                  dots: false,
                  arrows: false
              }
          },
          {
              breakpoint: 769,
              settings: {
                  arrows: false,
                  slidesToShow: 1,
                  slidesToScroll: 1
              }
          },
          {
              breakpoint: 481,
              settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                  arrows: false
              }
          }
          // You can unslick at a given breakpoint now by adding:
          // settings: 'unslick'
          // instead of a settings object
        ]
    });



    window.wow = new WOW({
        animateClass: 'animated',
        offset: 0,
        callback: function (box) {
        }
    });

    wow.init();


});


var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-36251023-1']);
_gaq.push(['_setDomainName', 'jqueryscript.net']);
_gaq.push(['_trackPageview']);

(function () {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();



document.onreadystatechange = function () {
    var state = document.readyState
    if (state == 'interactive') {
    } else if (state == 'complete') {
        setTimeout(function () {
            $('#load').animate({ 'opacity': '0' }, 'fast');

        }, 1000);
    }
}
