$(document).ready(function() {
    setFooter();
    studentsDetail();

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

    function studentsDetail() {
        $('#tb tr td .schoolname').on('click', function() {
            var sid = $(this).parent().parent().attr('id');
            var kid = $(this).parent().find('p').text();
            if (sid && !kid) {
                $.ajax({
                    url: '/studentinschool/',
                    type: 'GET',
                    data: { 'sid': sid },
                    success: function(arg) {
                        if (arg.status) {
                            students = JSON.parse(arg.data);
                            // console.log('ajax');
                            for (var i = 0; i < students.length; i++) {
                                $('#' + sid).find('td .student').append("<span class='badge'>" + students[i].fields.child_firstname + " " + students[i].fields.child_lastname + "</span><br>");
                            }
                        }
                    },
                });
            }
            $(this).parent().find('p').toggle();
        });
    };
})