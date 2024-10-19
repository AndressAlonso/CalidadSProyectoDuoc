$(document).ready(function() {
    $('#filterForm select').on('change', function() {
      $.ajax({
        url: $('#filterForm').attr('action'),
        data: $('#filterForm').serialize(), 
        type: 'GET',
        success: function(response) {
          $('#productos-list').html(response.html);
        }
      });
    });
  });