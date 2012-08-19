/* Publican JavaScript. */

$(document).ready(function() {

    $('.delete-filing').click(function(event) {
        var url = $(event.delegateTarget).attr('data-url');
        console.log('We want to delete the filing at', url);
    });

});
