// ready
$(document).on('ready', function () {
  'use strict';

  if($('.resonsive-tab').is(':visible')) {
    $('#dl-menu .vertical-menu').addClass('vertical-menu-responsive');
  }

  // Vertical icon-menu active script
  $('.hamburger').on('click', function () {
    if ($('.navbar-fixed-top').css('right') == '-100px') {
      $('.navbar-fixed-top').css('right', 0);
    }
    else {
      if ($('.navbar-fixed-top').css('overflow-y') == 'scroll') {
        $('.navbar-fixed-top').css('right', '-100px');
      }
    }
  });

  $('body').on('click', function (evt) {
    if ($('.navbar-fixed-top').css('z-index') == 10030) {
      if (evt.target.class == 'hamburger') {
        return;
      }
      if ($(evt.target).closest('.hamburger').length) {
        return;
      } else {
        if ($('.navbar-fixed-top').css('overflow-y') == 'scroll') {
          $('.navbar-fixed-top').animate({ right: '-100px' }, 'slow');
        }
      }
    }
  });

  // big-screen scroll for couple and story pages
  if ($.find('.bg-main-image-overlay-2').length) {
    $('.bg-main-image-overlay-2').scroll(function() {
      var scroll = $('.bg-main-image-overlay-2').scrollTop();
      if (scroll > 0) {
        $('#dl-menu').addClass('scroll-bg');
      } else {
        $('#dl-menu').removeClass('scroll-bg');
      }
    });
  }

  // slider
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

  window.wow = new WOW();
});

// onload
$(window).load(function () {
  // grid
  if ($.find('.gridlayout').length) {
    $('.gridlayout').isotope({
      // options...
      itemSelector: '.grid-item',
      masonry: {
        columnWidth: '.grid-item'
      }
    });
  }

  // page transition
  var $main = $('#pt-main'),
  $pages = $main.children('div.pt-page'),
  current = 0;

  $pages.each(function () {
    var $page = $(this);
    $page.data('originalClassList', $page.attr('class'));
    $(".page-top").addClass("display_none");
    $(".container-fluid").addClass("display_none");
  });

  $pages.eq(current).find(".page-top").removeClass("display_none");
  $pages.eq(current).find(".container").removeClass("display_none");
  $pages.eq(current).find(".container-fluid").removeClass("display_none");
  $pages.eq(current).addClass('pt-page-current');

  $('#dl-menu div').dlmenu({
    animationClasses: { in: 'dl-animate-in-2', out: 'dl-animate-out-2' },
    onLinkClick: function (el, ev) {}
  });
  $('#dl-menu').dlmenu({
    animationClasses: { in: 'dl-animate-in-2', out: 'dl-animate-out-2' },
    onLinkClick: function (el, ev) {}
  });

  // animate
  wow.init();

  // force render invisible wow elements
  setTimeout(function() {
    $('.pt-page .wow').each(function() {
      $(this).css('visibility', 'visible');
      $(this).css('animation-name', $(this).attr('data-class'));
    });
  }, 100);

  // Countdown
  if ($.find('.countdown').length) {
    $('.countdown').final_countdown();
  }
});


// analytics
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-91019716-1', 'auto');
ga('send', 'pageview');