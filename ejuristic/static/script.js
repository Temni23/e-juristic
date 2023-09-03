(function ($) {
    "use strict";

    $(document).ready(function () {

        if ($('.ant019_header-main-header li.dropdown ul').length) {
            $('.ant019_header-main-header li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

            //Dropdown Button
            $('.ant019_header-main-header li.dropdown .dropdown-btn').on('click', function () {
                $(this).prev('ul').slideToggle(500);
            });

            //Dropdown Menu / Fullscreen Nav
            $('.fullscreen-menu .ant019_header-navigation li.dropdown > a').on('click', function () {
                $(this).next('ul').slideToggle(500);
            });

            //Disable dropdown parent link
            $('.ant019_header-navigation li.dropdown > a').on('click', function (e) {
                e.preventDefault();
            });

            //Disable dropdown parent link
            $('.ant019_header-main-header .ant019_header-navigation li.dropdown > a,.hidden-bar .side-menu li.dropdown > a').on('click', function (e) {
                e.preventDefault();
            });
        }
    });
})(jQuery);

/*! version : 1.0.0 */

jQuery( document ).ready(function($) {

});

(function ($) {
    'use strict';

    $(window).on('load', function () {



    });

})(jQuery);
