/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true */
/*global jQuery:false, document:false, location:false */

(function ($) {
    $(document).ready(function () {
        $('#main-nav').superfish({
            delay: 500,
            animation: {opacity: 'show', height: 'show'},
            speed: 'fast',
            autoArrows: false
        });
        $('img.team-image').popover({
            trigger: 'hover'
        });
        $(".bannertabs").tabs('.bannerbar > div.banner', {
            effect: 'fade',
            fadeOutSpeed: 1000,
            rotate: true
        }).slideshow({
            autoplay: true,
            interval: 6000,
            clickable: false
        });
        var infotabs = $('div.infopane').hide();
        var current = $('#infopane-1').fadeIn('slow');
        $('a[data-appui="infotabs"]').on('hover', function () {
            var target = $(this).data('target');
            current = $(target);
            infotabs.not(current).fadeOut('fast');
            infotabs.promise().done(function () {
                current.fadeIn('slow');
            });
        });
        $('#project-gallery').scrollable().navigator();
        $("#project-gallery .items img").on('click', function () {
            if ($(this).hasClass("active")) { return; }
            var url = $(this).data('image-url');
            var width = $(this).data('image-width');
            var height = $(this).data('image-height');
            var wrap = $("#image-wrapper").fadeTo("medium", 0.5);
            var img = new Image();
            img.onload = function () {
                wrap.fadeTo("fast", 1);
                wrap.find("img").attr({
                    "src": url,
                    "width": width,
                    "height": height
                });
            };
            img.src = url;
            $(".items img").removeClass("active");
            $(this).addClass("active");
        }).filter(":first").click();
        $("a.popoverLogin").prepOverlay(
        {
            subtype: 'ajax',
            filter: '#content>*',
            formselector: 'form#login_form',
            noform: 'redirect',
            redirect: function (overlay, responseText) {
                var href = location.href;
                if (href.search(/pwreset_finish$/) >= 0) {
                    return href.slice(0, href.length - 14) + 'logged_in';
                } else {
                    // look to see if there has been a server redirect
                    var newTarget = $("<div>").html(responseText).find("base").attr("href");
                    if ($.trim(newTarget) && newTarget !== location.href) {
                        return newTarget;
                    }
                    // if not, simply reload
                    return href;
                }
            }
        }
    );
    });
}(jQuery));