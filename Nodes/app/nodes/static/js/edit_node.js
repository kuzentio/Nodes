
$(document).ready(function() {
    $('.weight').hide();

    $('.node-information').each(function () {

        if ($(this).find('.node').is(':checked')) {
            $(this).find('input.weight').show()
        }
        if ($(this).find('.node').is(':disabled')) {
            $(this).find('input.weight').hide()
        }
    });

    $('.node').change(function () {
        if ($(this).is(':checked')) {

            $(this).parent().find('.weight').show();
        }
        else {
            $(this).parent().find('.weight').hide();
        }
    });

    $('#submit').click(function () {

        $('.node-information').each(function () {

            if (!$.isNumeric($(this).find('input.weight').val())){
                $(this).remove()
            }

        })
    });


});


