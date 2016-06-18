/**
 *
 * Binds ajax api calls to buttons for lifestudy pages
 *
 */

$(window).ready(function(e) {
  // Bind click event to all delete buttons to ajax delete summaries
  $('.delete').on('click', function(ev) {
    var btn = $(this);
    if (!window.confirm('Are you sure you want to delete this life study summary?')) {
      return false;
    }
    // send ajax request
    $.ajax({
      url: '/api/summaries/' + btn.attr('id').split('-')[1] + '/',
      data: {deleted: true},
      type: 'POST',
      success: function(response, status) {
        // remove element on page
        btn.parent().remove();
      }
    });

    return false;
  });
});
