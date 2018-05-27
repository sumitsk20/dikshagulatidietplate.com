//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".navbar").offset().top > 500) {
        $(".appointment-form-tab").fadeIn("fast");
        $(".scrollToTop").fadeIn();
    } else {
        $(".appointment-form-tab").fadeOut("fast");
        $(".scrollToTop").fadeOut();
    }
        if($(window).width() >= 768) {
            if ($(".navbar").offset().top > 20) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
            $(".logo-img").css({"max-height": "50px","margin-top": "0px","transition":"all 0.5s ease","opacity":"1"});
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
            $(".logo-img").css({"max-height": "61px","margin-top": "-5px","transition":"all 0.5s ease"});
        }

    } else{
            $(".logo-img").css({"max-height": "50px","margin-top": "0px","transition":"all 0.5s ease","opacity":"1"});
        }

});
//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {

    $('a.page-scroll').bind('click', function(event) {
        $('html, body').stop().animate({
            scrollTop:0
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
