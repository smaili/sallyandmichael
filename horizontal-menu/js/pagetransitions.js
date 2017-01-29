var PageTransitions = (function () {

    var $main = $('#pt-main'),
		$pages = $main.children('div.pt-page'),
		animcursor = 1,
		pagesCount = $pages.length,
		current = 0,
		isAnimating = false,
		endCurrPage = false,
		endNextPage = false,
		animEndEventNames = {
		    'WebkitAnimation': 'webkitAnimationEnd',
		    'OAnimation': 'oAnimationEnd',
		    'msAnimation': 'MSAnimationEnd',
		    'animation': 'animationend'
		},
		// animation end event name
		animEndEventName = animEndEventNames[Modernizr.prefixed('animation')],
		// support css animations
		support = Modernizr.cssanimations;

    function init() {
        $pages.each(function () {
            var $page = $(this);
			
            $page.data('originalClassList', $page.attr('class'));
			$(".page-top").addClass("display_none");
			  $(".container-fluid").addClass("display_none");
        });
$pages.eq(current).find(".page-top").removeClass("display_none");
		$pages.eq(current).find(".container-fluid").removeClass("display_none");
        $pages.eq(current).addClass('pt-page-current');

        $('#dl-menu div').dlmenu({
            animationClasses: { in: 'dl-animate-in-2', out: 'dl-animate-out-2' },
            onLinkClick: function (el, ev) {
                ev.preventDefault();
                
                if (el.hasClass("hover_active") || el.hasClass("other-menu")) {
                    return false;
                }
                else {
                    nextPage(el.data('animation') - 1);
                }
            }
        });
        $('#dl-menu').dlmenu({
            animationClasses: { in: 'dl-animate-in-2', out: 'dl-animate-out-2' },
            onLinkClick: function (el, ev) {
                ev.preventDefault();
                nextPage(el.data('animation') - 1);
            }
        });



    }

    function nextPage(options) {
        var animation = (options.animation) ? options.animation : options;
        if (isAnimating) {
            return false;
        }

        isAnimating = true;

        var $currPage = $pages.eq(current);

        current = animation;

        var $nextPage = $pages.eq(current).addClass('pt-page-current'),
            outClass = 'pt-page-moveToLeft';
        inClass = 'pt-page-moveFromRight';

 $(".page-top").addClass("display_none");
	  $(".container-fluid").addClass("display_none");
		$pages.eq(current).find(".container-fluid").removeClass("display_none");
        $pages.eq(current).addClass('pt-page-current');
        $currPage.addClass(outClass).on(animEndEventName, function () {
            $currPage.off(animEndEventName);
            endCurrPage = true;
            if (endNextPage) {
                onEndAnimation($currPage, $nextPage);
            }
        });
        $('.the-people-slider').slick("slickNext");
        $('.ceremony-slider').slick("slickNext");
        $nextPage.addClass(inClass).on(animEndEventName, function () {
            $nextPage.off(animEndEventName);
            endNextPage = true;
            if (endCurrPage) {
                onEndAnimation($currPage, $nextPage);
            }
        });

        if (!support) {
            onEndAnimation($currPage, $nextPage);
        }
    }

    function onEndAnimation($outpage, $inpage) {
        endCurrPage = false;
        endNextPage = false;
        resetPage($outpage, $inpage);
        isAnimating = false;
		  if(  $(".navbar-fixed-top").css('overflow-y')=='scroll'){
					     $(".navbar-fixed-top").animate({right:'-100px'}, 'slow');
						}
			$('.gridlayout').isotope({ filter: '*' });
    }

    function resetPage($outpage, $inpage) {
        $outpage.attr('class', $outpage.data('originalClassList'));
        $inpage.attr('class', $inpage.data('originalClassList') + ' pt-page-current');
    }

    init();

    return {
        init: init,
        nextPage: nextPage,
    };

})();