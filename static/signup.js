var success_text = '<h4> style="color: green;">The user is successfully created!<i class="material-icons">done</i><br>Forwarding to login page...</h4>';
var initial_text = "<h4>Please input the following information to create a new account</h4>";
var div_avatar = "#div_id_avatar";
var avatar = "id_avatar";
var this_form = "#signup_form";
var max_file_size = 2000000;

function fileValidation() {
    var fileInput = document.getElementById(avatar);
    var filePath = fileInput.value;

    var allowedExtensions =
            /(\.jpg|\.jpeg|\.png|\.gif)$/i;

    if (!(fileInput.files && fileInput.files[0])) {
        return true;
    }

    if (!allowedExtensions.exec(filePath)) {
        $(div_avatar).addClass('invalid_file_format');
        fileInput.value = '';
        return false;
    }
    if(fileInput.files[0].size > max_file_size){
        $(div_avatar).addClass('invalid_file_size');
        fileInput.value = '';
        return false;
    }

        if (fileInput.files && fileInput.files[0]) {
//            var reader = new FileReader();
//            reader.onload = function(e) {
//                document.getElementById(
//                    'imagePreview').innerHTML =
//                    '<img src="' + e.target.result
//                    + '"/>';
//            };
//            reader.readAsDataURL(fileInput.files[0]);
            return true;
        }
}
function removeWarnings(){
    if ($(div_avatar).hasClass("invalid_file_size")){
        $(div_avatar).removeClass("invalid_file_size");
    }
        if ($(div_avatar).hasClass("invalid_file_format")){
        $(div_avatar).removeClass("invalid_file_format");
    }
        if ($(div_avatar).hasClass("file_attention")){
        $(div_avatar).removeClass("file_attention");
    }
}

$(document).ready(function () {
    var upper_notice = $('#upper_notice');
    upper_notice.html(initial_text);
    $(this_form).on("submit", function(){
        removeWarnings();
        if (!fileValidation()){
            return false;
        }
        var formData = new FormData(this);
        $.ajax({
            url: $(this_form).data("url"),
            type: 'POST',
            data: formData,
            cache:false,
            contentType: false,
            processData: false,
            success: function(data) {
                var form_without_button = data['form_html'].replace(/<form .*?>/, "");
                form_without_button = form_without_button.replace(/<\/form>/, "");
                var form_with_button = form_without_button + "<button class=\"form_auth_button\" type=\"submit\" name=\"button\" >Create user</button>";
                $(this_form).html(form_with_button);
                if (!(data.success)) {
                    $('#hint_id_password2').text("");
                    $(div_avatar).addClass("file_attention");
                }
                else {
                    upper_notice.html(success_text);
                    var url = window.location.href;
                    var pattern = /(.*\/{2})(.*?\/)(.*)/i;
                    var result = url.match(pattern);
                    var new_url = result[1] + result[2] + "login";
                    setTimeout(()=>{window.location.replace(new_url);}, 7000);
                }
            },
            error: function (response) {
                console.log(response.responseText);
            }
        });
        return false;
    });
});
