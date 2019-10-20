// ready

// tabs
$('.card-header .nav-tabs .nav-link').on('click', function (evt) {
  evt.preventDefault();
  evt.stopPropagation();

  var navLink = $(this);
  var navTabs = navLink.parents('.nav-tabs');
  var navIndex = navLink.parents('.nav-item').index();
  var navBlocks = navLink.parents('.card').find('.card-block');

  if (navLink.hasClass('active')) {
    return;
  }

  navTabs.find('.nav-link').removeClass('active');
  navLink.addClass('active');
  navBlocks.addClass('d-none');
  navBlocks.eq(navIndex).removeClass('d-none');
});

// buttons
$('#inviteModal .btn-primary').on('click', function (evt) {
  evt.preventDefault();
  evt.stopPropagation();

  var button = $(this);
  var modal = button.parents('.modal');

  button.addClass('disabled');

  var data = {};
  modal
    .find('.modal-group').not('.d-none')
    .find('input, textarea')
    .each(function(i, e) {
      var el = $(e);
      data[el.attr('name')] = el.val()
    });

  modal.find('.alert').html('').addClass('d-none');

  $.post(button.data('action-href'), data, function(response) {
    try {
      var parse = JSON.parse(response);
      if (parse.status == 'error') {
        for (var name in parse.errors) {
          var input = modal.find('[name="' + name + '"]');
          input.siblings('.form-text.text-danger').html(parse.errors[name]);
        }

        if (parse.mailfailed) {
          modal.find('.alert-danger').removeClass('d-none').html(parse.mailfailed);
        } else if (parse.savefailed) {
          modal.find('.alert-danger').removeClass('d-none').html(parse.savefailed);
        }
      } else {
        modal.find('.alert-success').removeClass('d-none').html(parse.success);
      }
    } catch (ex) {
    }

    // if we get here, there must've been an error :(
    // show popup
    button.removeClass('disabled');
  });
});