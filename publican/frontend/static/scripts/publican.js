/* Publican JavaScript. */

$(document).ready(function() {

    var reload_page = function() {
        location.reload();
    };

    $('.delete-filing').click(function(event) {
        var url = $(event.delegateTarget).attr('data-url');
        $.ajax({url: url, type: 'DELETE', success: reload_page});
    });

});
