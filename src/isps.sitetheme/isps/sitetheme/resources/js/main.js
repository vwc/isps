/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, window:false, location:false */

(function ($) {
    $(document).ready(function () {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) {
            // it's not realistic to think we can deal with all the bugs
            // of IE 6 and lower. Fortunately, all this is just progressive
            // enhancement.
            return;
        }
        var current, menuboxes = $('ul.megamenu');
        $('a.megamenu-toggle').on('click', function (e) {
            var target_menu = $(this).data('appui-target');
            current = $(target_menu);
            menuboxes.not(current).fadeOut('slow');
            current.toggle('slow');
            e.preventDefault();
        });
        $(".bannertabs").tabs('.bannerbar > div.banner', {
            effect: 'fade',
            fadeOutSpeed: 1000,
            rotate: true
        }).slideshow({
            autoplay: true,
            interval: 6000
        });
        $('#infotabs').tabs('div.infopanes > div.infopane', {
            tabs: 'li.infotab'
        });
        $("#project-gallery .items img").on('click', function () {
            if ($(this).hasClass("active")) { return; }
            var url = $(this).data('image-url');
            var wrap = $("#image-wrapper").fadeTo("medium", 0.5);
            var img = new Image();
            img.onload = function () {
                wrap.fadeTo("fast", 1);
                wrap.find("img").attr("src", url);
            };
            img.src = url;
            $(".items img").removeClass("active");
            $(this).addClass("active");
        }).filter(":first").click();
    });
}(jQuery));