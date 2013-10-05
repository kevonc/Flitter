var checkCharacterCount = function() {
  if ($('#content').val().length > 200) {
    $('#content').css('color', 'red');
    $('#message').html('<p>You have entered more than 200 characters. Please shorten your post.</p>');
    $('#newPostBtn').attr('disabled', 'disabled');
  } else {
    $('#content').css('color', '#3d3d3d');
    $('#message').html('');
    $('#newPostBtn').removeAttr('disabled');
  }
};

$(function() {
  $('#content').keyup(function(){
    checkCharacterCount();
  });
});