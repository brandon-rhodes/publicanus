/* Publican JavaScript. */

$(document).ready(function() {

    var reload_page = function() {
        location.reload();
    };

    $('.delete-filing').click(function(event) {
        var url = $(event.delegateTarget).attr('data-url');
        $.ajax({url: url, type: 'DELETE', success: reload_page});
    });

    var create_input = null;

    $('.create-filing').click(function(event) {
        if (create_input !== null) {
            create_input.show();
            create_input.focus();
            return;
        }

        var go = function(e) {
            val = create_input.val();
            if (!/^[0-9]+\/[0-9]+\/[0-9]+/.test(val))
                return;
            var url = $('.create-filing').attr('data-url');
            var json = eval($('.create-filing').attr('data-json'));
            console.log(json);
            create_input.hide();
        };

        create_input = $('<input>');
        $('.create-filing').parent().after(create_input);
        create_input.datepicker({
            minDate: '1/1/1990', maxDate: '+1d', onSelect: go
        });
        create_input.keypress(function(e) {
            if (e.which === 13)  // enter key
                go();
        });
        create_input.focus();
    });
});
