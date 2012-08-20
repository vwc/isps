/*jslint white:false, onevar:true, undef:true, nomen:true, eqeqeq:true, plusplus:true, bitwise:true, regexp:true, newcap:true, immed:true, strict:false, browser:true *//*global jQuery:false, document:false, window:false, location:false */(function(e) {
    e(document).ready(function() {
        if (jQuery.browser.msie && parseInt(jQuery.browser.version, 10) < 7) return;
        var t, n = e("ul.megamenu");
        e("a.megamenu-toggle").on("click", function(r) {
            var i = e(this).data("appui-target");
            t = e(i);
            n.not(t).fadeOut("slow");
            t.toggle("slow");
            r.preventDefault();
        });
        e(".bannertabs").tabs(".bannerbar > div.banner", {
            effect: "fade",
            fadeOutSpeed: 1e3,
            rotate: !0
        }).slideshow({
            autoplay: !0,
            interval: 6e3
        });
        e("#infotabs").tabs("div.infopanes > div.infopane", {
            tabs: "li.infotab"
        });
        e("#project-gallery .items img").on("click", function() {
            if (e(this).hasClass("active")) return;
            var t = e(this).data("image-url"), n = e("#image-wrapper").fadeTo("medium", .5), r = new Image;
            r.onload = function() {
                n.fadeTo("fast", 1);
                n.find("img").attr("src", t);
            };
            r.src = t;
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