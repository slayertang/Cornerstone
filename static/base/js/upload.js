$(document).ready(function() {
    $('#submit').on('click', function() {
        var a = $('#fileinput').val();
        if (a) {
            $('#tip').show();
        }
    });
});