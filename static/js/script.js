$(document).ready(function () {
    $('.header__user-link').on('click', function () {
        if ( $('.header__popup').hasClass('active') ) {
            $('.header__popup').removeClass('active');
        } else {
            $('.header__popup').addClass('active');
        }
    });

    $('.message').css({
        opacity: 1,
        transform: 'translateY(0)'
    });

    $('button[type="submit"]').on('click', function () {
        $(this).css("pointer-events", "none");
    });
});