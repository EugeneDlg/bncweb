var success_text = "Changes saved " + '<i class="material-icons">done</i>' + " Forwarding to login page...";
var initial_text = "Edit your personal information";

$(document).ready(function () {
    var upper_notice = $('#upper_notice');
//    upper_notice.text(initial_text);
    upper_notice.html(initial_text);
    upper_notice.attr("style", "color: green; font-weight: bold;");
$("#edit_form").on("submit", function(){
$.ajax({
    url: $("#edit_form").data("url"),
    dataType: 'json',
    method: 'post',
    data: $(this).serialize(),
    success: function(data) {
        if (!(data.success)) {
        alert ("SUCCESS");
    	var form_without_button = data['form_html'].replace(/<form .*?>/, "");
    	form_without_button = form_without_button.replace(/<\/form>/, "");
    	var form_with_button = form_without_button + "<button class=\"edit_button\" type=\"submit\" name=\"button\" >Modify user</button>";
    	console.log(form_with_button);
        $('#edit_form').html(form_with_button);
        $('#hint_id_password2').text("");
        }
        else {
            // Here you can show the user a success message or do whatever you need
            //$('#signup_form').find('.success-message').show();
//            success_item.style.display = '';
//            initial_notice.style.display = 'none';
            var url = window.location.href;
            var pattern = /(.*\/{2})(.*?\/)(.*)/i;
            var result = url.match(pattern);

        }
    },
    error: function (response) {
        console.log(response.responseJSON.errors);
    }
});
return false;
});

});
