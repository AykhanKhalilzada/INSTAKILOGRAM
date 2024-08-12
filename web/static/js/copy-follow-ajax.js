// script.js

function copyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.top = 0;
  textArea.style.left = 0;
  textArea.style.width = "1px";
  textArea.style.height = "1px";
  textArea.style.opacity = 0;
  document.body.appendChild(textArea);
  textArea.select();
  document.execCommand("copy");
  document.body.removeChild(textArea);
}

document.addEventListener("DOMContentLoaded", function() {
  var shareProfileButton = document.getElementById("shareProfileButton");

  if (shareProfileButton) {
      shareProfileButton.addEventListener("click", function() {
          var profileUrl = this.getAttribute("data-url");
          var port = this.getAttribute("data-port-url");
          var fullUrl = port + profileUrl;

          if (profileUrl) {
              copyTextToClipboard(fullUrl);
              alert("Profile URL copied to clipboard!");
          } else {
              alert("Failed to get profile URL.");
          }
      });
  }
});



$(document).ready(function() {
    $('.ajax-button-following-profile').click(function() {
      const button = $(this);
      const following_id = button.attr('following_id');
      const csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
      
      const followerCountElement = $('.following_info .ajax');
      let currentCount = parseInt(followerCountElement.text());
      
      $.ajax({
          url: "/create/follow/",
          type: "POST",
          dataType: "json",
          data: {
              following_id: following_id,
              csrfmiddlewaretoken: csrfmiddlewaretoken
          },
          success: (data) => {
            if (button.text() == "Follow") {
              button.closest('.button').removeClass('follow').addClass('following');
              button.text("Following");
              followerCountElement.text(currentCount + 1);
            }
            else {
              button.closest('.button').removeClass('following').addClass('follow');
              button.text("Follow");
              followerCountElement.text(currentCount - 1);
            }
            console.log(data);
          },
          error: (error) => {
            console.log(error);
          }
      });
    });
});