var initial_text = "<h4>Please input the following information to create a new account</h4>";
var success_text = initial_text + '<br><h5 style="color: green;">The user is successfully created!<i class="material-icons">done</i><br>Forwarding to login page...</h5>';

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
    var wait_item = document.getElementById('wait');
    wait_item.style.display = 'none';
    upper_notice.html(initial_text);
    $(this_form).on("submit", function(){
        wait_item.style.display = '';
        var fileInput = document.getElementById(avatar);
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
                wait_item.style.display = 'none';
                var form_without_button = data['form_html'].replace(/<form .*?>/, "");
                form_without_button = form_without_button.replace(/<\/form>/, "");
                var form_with_button = form_without_button +
                "<div class=\"justify-content-center  text-center\"><button class=\"btn btn-primary\"" +
                " type=\"submit\" name=\"button\" >Submit changes</button></div>";
                $(this_form).html(form_with_button);
                if (!(data.success)) {
                    $('#hint_id_password2').text("");
                    $(div_avatar).addClass("file_attention");
                }
                else {
                    if (fileInput.files && fileInput.files[0]) {
                        av_image.src = URL.createObjectURL(fileInput.files[0]);
                    }
                    var upper_notice = $('#upper_notice');
                    upper_notice.html(success_text);
                    $('html, body').animate({ scrollTop: 0 }, 'fast');
                    var url = window.location.href;
                    var pattern = /(.*\/{2})(.*?\/)(.*)/i;
                    var result = url.match(pattern);
                    var new_url = result[1] + result[2] + "login";
                    setTimeout(()=>{window.location.replace(new_url);}, 8000);

                }
            },
            error: function (response) {
                wait_item.style.display = 'none';
                console.log(response.responseText);
            }
        });
        return false;
    });
});
