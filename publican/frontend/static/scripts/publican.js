/* Publican JavaScript. */

$(document).ready(function() {

    var reload_page = function() {
        location.reload();
    };

    $('.delete-filing').click(function(event) {
        var url = $(event.delegateTarget).attr('data-url');
        $.ajax({url: url, type: 'DELETE', success: reload_page});
    });

    var $create_button = $('.create-filing');
    var $create_input = null;

    var ignore_submit = false;

    $create_button.click(function(event) {
        if ($create_input !== null) {
            $create_input.show();
            $create_input.focus();
            return;
        }

        var go = function(e) {
            var val = $create_input.val();
            if (!/^[0-9]+\/[0-9]+\/[0-9]+/.test(val))
                return;

            if (ignore_submit)
                return;

            ignore_submit = true;

            var url = $('.create-filing').attr('data-url');
            var json = $('.create-filing').attr('data-json');

            var data = $.parseJSON(json);
            data.date = val;

            $.ajax({
                url: url,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function() {
                    ignore_submit = false;
                    reload_page();
                },
                error: function() {
                    ignore_submit = false;
                }
            });
            $create_input.hide();
        };

        $create_input = $('<input>');
        $create_button.parent().after($create_input);
        $create_input.datepicker({
            minDate: '1/1/1990', maxDate: '+1d', onSelect: go,
            appendText: '<br>When did you file?'
        });
        $create_input.keypress(function(e) {
            if (e.which === 13)  // enter key
                go();
        });
        $create_input.focus();
    });
});
