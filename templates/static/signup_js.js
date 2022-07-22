$(document).ready(function () {
	success_notice = document.getElementById('success_notice');
	success_notice.style.display = '';
	success_notice = document.getElementById('initial_notice');

    initial_notice.style.display = 'none';
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
            success_item.style.display = '';
            initial_notice.style.display = 'none';
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
