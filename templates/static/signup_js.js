var success_text = "The user is successfully created! " + '<i class="material-icons">done</i>' + " Forwarding to login page...";
var initial_text = "Please input the following information to create a new account";

$(document).ready(function () {
    var upper_notice = $('#upper_notice');
//    upper_notice.text(initial_text);
    upper_notice.html(initial_text);
    upper_notice.attr("style", "color: green; font-weight: bold;");
$("#signup_form").on("submit", function(){
$.ajax({
    url: "{% url 'signup' %}",
    dataType: 'json',
    method: 'post',
    data: $(this).serialize(),
    success: function(data) {
        if (!(data.success)) {
    	var form_without_button = data['form_html'].replace(/<form .*?>/, "");
    	form_without_button = form_without_button.replace(/<\/form>/, "");
    	var form_with_button = form_without_button + "<button class=\"form_auth_button\" type=\"submit\" name=\"button\" >Create user</button>";
    	console.log(form_with_button);
        $('#signup_form').html(form_with_button);
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
            var new_url = result[1] + result[2] + "login";
            setTimeout(()=>{window.location.replace(new_url);}, 3000);

        }
    },
    error: function (response) {
        console.log(response.responseJSON.errors);
    }
});
return false;
});

});
