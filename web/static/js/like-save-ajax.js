$(document).ready(function() {
  $('.ajax-like-button').click(function() {
    const button = $(this);
    const postId = button.attr('post_id');
    const csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: "/create/like/",
      type: "POST",
      dataType: "json",
      data: {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        post_id: postId
      },
      success: (data) => {
        if (button.find('img').attr('alt') == 'Like') {
            button.find('img').attr('src', '/static/icons/liked.png').attr('alt', 'Liked');
        }
        else {
            button.find('img').attr('src', '/static/icons/like.png').attr('alt', 'Like');
        }
        console.log(data);
      },
      error: (error) => {
        console.log(error);
      }
    });
  });
});


$(document).ready(function() {
  $('.ajax-save-button').click(function() {
      const button = $(this);
      const postId = button.attr('post_id');
      const csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: "/create/save/",
      type: "POST",
      dataType: "json",
      data: {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        post_id: postId
      },
      success: (data) => {
        if (button.find('img').attr('alt') == 'Save') {
            button.find('img').attr('src', '/static/icons/saved.png').attr('alt', 'Saved');
        }
        else {
          button.find('img').attr('src', '/static/icons/Save.png').attr('alt', 'Save');
        }
        console.log(data);
      },
      error: (error) => {
        console.log(error);
      }
    });
  });
});


$(document).ready(function() {
  $('.ajax-follow-button').click(function() {
      const button = $(this);
      const followingId = button.attr('following_id');
      const csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: "/create/follow/",
      type: "POST",
      dataType: "json",
      data: {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        following_id: followingId
      },
      success: (data) => {
        if (button.text() == "Follow") {
          button.hide();
        }
        console.log(data);
      },
      error: (error) => {
        console.log(error);
      }
    });
  });
});

$(document).ready(function() {
  $('.ajax-commment-delete-button').click(function() {
      const button = $(this);
      const deletion_token = button.attr('deletion_token');
      const csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

    $.ajax({
      url: "/create/comment/",
      type: "POST",
      dataType: "json",
      data: {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        deletion_token: deletion_token
      },
      success: (data) => {
        if (button.text() == "Delete") {
          button.text("Deleted");
        }
        console.log(data);
      },
      error: (error) => {
        console.log(error);
      }
    });
  });
});