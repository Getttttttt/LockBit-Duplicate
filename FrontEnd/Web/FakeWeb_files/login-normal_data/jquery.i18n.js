(function($) {
    $.i18n = function(messages) {
        $('[i18n]').each(function () {
            if ($(this).val() != null && $(this).val() != '') {
                $(this).val(messages[$(this).attr('i18n')]);
            }
            if ($(this).html() != null && $(this).html() != '') {
                $(this).html(messages[$(this).attr('i18n')]);
            }
            if ($(this).attr('placeholder') != null && $(this).attr('placeholder') != '') {
                $(this).attr('placeholder', messages[$(this).attr('i18n')]);
            }
        });
        $('body').show();
    };
} (jQuery));