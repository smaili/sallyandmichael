(function ($) {
	'use strict';


  if ($.find('#frm').length) {
    var submitted = false;
    $('#frm').submit(function(evt) {
      // prevent multiple submissions
      if (submitted) {
        return false;
      }

      submitted = true;
      $(this).addClass('submitted');
    });

    $('.form-group input').on('focus', function(evt) {
      var input = $(this);
      input.addClass('dirty');
    });

    $('.form-group input').on('blur', function(evt) {
      var input = $(this);
      if ($.trim(input.val()) !== '') {
        input.addClass('dirty').removeClass('static');
      } else {
        input.removeClass('dirty').removeClass('static');
      }
    });
  }
})(jQuery);