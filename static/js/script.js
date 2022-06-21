$(document).ready(function () {
    $('.header__user-link').on('click', function () {
        if ( $('.header__popup').hasClass('active') ) {
            $('.header__popup').removeClass('active');
        } else {
            $('.header__popup').addClass('active');
        }
    });
});