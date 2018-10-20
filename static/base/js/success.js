$(document).ready(function() {
    setFooter();

    function setFooter() {
        var browserH = $(window).height();
        var h = $('.content').height();
        var topH = $('.content').offset().top;
        var scroll = $(document).scrollTop();
        var footer = $('.footer').height();
        // console.log(browserH);
        // console.log(h);
        // console.log(topH);
        // console.log(scroll);
        // console.log(footer);
        var bottomD = browserH - (h + topH - scroll) - footer - 60;
        // console.log(bottomD);
        $('.content').css('padding-bottom', bottomD);
    };
})