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