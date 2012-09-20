/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true *//*global jQuery:false, document:false, location:false */(function(e) {
    e(document).ready(function() {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) return;
        e("#main-nav").superfish({
            delay: 1e3,
            animation: {
                opacity: "show",
                height: "show"
            },
            speed: "slow",
            autoArrows: !1
        });
        e("img.team-image").popover();
        e(".bannertabs").tabs(".bannerbar > div.banner", {
            effect: "fade",
            fadeOutSpeed: 1e3,
            rotate: !0
        }).slideshow({
            autoplay: !0,
            interval: 6e3,
            clickable: !1
        });
        var t = e("div.infopane").hide(), n = e("#infopane-1").fadeIn("slow");
        e('a[data-appui="infotabs"]').on("hover", function() {
            var r = e(this).data("target");
            n = e(r);
            t.not(n).fadeOut("fast");
            t.promise().done(function() {
                n.fadeIn("slow");
            });
        });
        e("#project-gallery").scrollable().navigator();
        e("#project-gallery .items img").on("click", function() {
            if (e(this).hasClass("active")) return;
            var t = e(this).data("image-url"), n = e(this).data("image-width"), r = e(this).data("image-height"), i = e("#image-wrapper").fadeTo("medium", .5), s = new Image;
            s.onload = function() {
                i.fadeTo("fast", 1);
                i.find("img").attr({
                    src: t,
                    width: n,
                    height: r
                });
            };
            s.src = t;
            e(".items img").removeClass("active");
            e(this).addClass("active");
        }).filter(":first").click();
        e("a.popoverLogin").prepOverlay({
            subtype: "ajax",
            filter: common_content_filter,
            formselector: "form#login_form",
            noform: "redirect",
            redirect: function(t, n) {
                var r = location.href;
                if (r.search(/pwreset_finish$/) >= 0) return r.slice(0, r.length - 14) + "logged_in";
                var i = e("<div>").html(n).find("base").attr("href");
                return e.trim(i) && i !== location.href ? i : r;
            }
        });
    });
})(jQuery);