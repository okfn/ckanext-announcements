$( document ).ready(function() {

    $(document).on('click', 'form button[type=submit].announcement-submit-button', function(e) {
        $this = $(this);
        $form = $(e.target).parents('form');
        errors = [];
        $message = $form.find('.announcement-message-input textarea');
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
            $('.announcement-form-error').html('<strong>Please fix the following errors:</strong><ul><li>' + errors.join('</li><li>') + '</li></ul>');
            $('.announcement-form-error').show();
            // Scroll to error message
            $('.modal-body').animate({
                scrollTop: $('.announcement-form-error').position().top
            }, 500);
        }
    });

    // hide error div on modal hide to start fresh next time
    $('.announcement-form-modal').on('hide.bs.modal', function () {
        $('.announcement-form-error').hide();
        // Reset any custom styling
        $('.modal-dialog').css('overflow-y', '');
    });

    // add a cookie to remember if user closed any announcement
    $(document).on('click', '.announcement-close-button', function(e) {
        var announcement_id = $(this).data('announcement-id');
        var storage_name = 'announcement_closed_' + announcement_id;
        var expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 30);  // Set expiration date to 7 days from now
        var item = {
            value: 'true',
            expiry: expirationDate.getTime()
        };
        localStorage.setItem(storage_name, JSON.stringify(item));
    });

    // Show announcements that haven't been previously closed by the user
    $('.announcement').each(function(i, obj) {
        var announcement_id = $(obj).data('announcement-id');
        var storage_name = 'announcement_closed_' + announcement_id;
        var st = localStorage.getItem(storage_name);
        var now = new Date();
        if (st === null ) {
            // If the item is not in the storage show the announcement
            $(obj).show();
        }
        // remove the storage key if expired
        else {
            var item = JSON.parse(localStorage.getItem(storage_name));
            if (now.getTime() > item.expiry) {
                localStorage.removeItem(storage_name);
            }
        }
    });
});