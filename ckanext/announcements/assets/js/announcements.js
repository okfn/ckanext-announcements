$( document ).ready(function() {

    $(document).on('click', 'form button[type=submit].announcement-submit-button', function(e) {
        $this = $(this);
        $form = $(e.target).parents('form');
        errors = [];
        $message = $form.find('.announcement-message-input');
        if (! $message.val()) {
            errors.push('Error, a "message" is required');
        }

        $dates = $form.find('.announcement-date-input');
        $dates.each(function(i, obj) {
            if (! obj.value) {
                errors.push('Error, a date is required for "' + obj.name + '"');
            }
        });

        if (errors.length > 0) {
            e.preventDefault(); //prevent the default action
            $('.announcement-form-error').html(errors.join('<br/>'));
            $('.announcement-form-error').show();
        }
    });

    // hide error div on modal hide to start fresh next time
    $('.announcement-form-modal').on('hide.bs.modal', function () {
        $('.announcement-form-error').hide();
    })
});