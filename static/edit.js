var initial_text = upper_label;
var success_text = initial_text + "<br>" + '<h4 style="color: green;">Changes saved <i class="material-icons">done</i></h4>';
var upper_notice = $('#upper_notice');
var div_avatar = "#div_id_avatar";
var avatar = "id_avatar";
var main_form = "#edit_form";
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
//        var reader = new FileReader();
//        reader.readAsDataURL(fileInput.files[0]);
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
function initial_text_show(){
     upper_notice.html(initial_text);
}

function setImageVisible(id, visible) {
    var img = document.getElementById(id);
    img.style.visibility = (visible ? 'visible' : 'hidden');
}

$(document).ready(function () {
    wait_item = document.getElementById('wait');
    wait_item.style.display = 'none';
    wait_item2 = document.getElementById('wait2');
    wait_item2.style.display = 'none';
    document.getElementById("delete_button").disabled = !is_avatar_available;
    initial_text_show();
    $(main_form).on("submit", function(){
        wait_item.style.display = '';
        var fileInput = document.getElementById(avatar);
        initial_text_show();
        removeWarnings();
        if (!fileValidation()){
            return false;
        }
        var formData = new FormData(this);
        $.ajax({
            url: $(this).data("url"),
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
                $(main_form).html(form_with_button);
//                if (fileInput_.files && fileInput_.files[0]) {
//                $(main_form).append('avatar', fileInput_.files[0],fileInput_.files[0]);
//                }
                if (!(data.success)) {
                    $('#hint_id_password2').text("");
                    $(div_avatar).addClass("file_attention");
                }
                else {
                    if (fileInput.files && fileInput.files[0]) {
                        av_image.src = URL.createObjectURL(fileInput.files[0]);
                        document.getElementById("delete_button").disabled = false;
                    }
                    upper_notice.html(success_text);
                }
            },
            error: function (response) {
                wait_item.style.display = 'none';
                console.log(response.responseText);
            }
        });
        return false;
    });

    $("#delete_av_form").on("submit", function(){
        wait_item2.style.display = '';
        $.ajax({
            url: $(this).data("url"),
            method: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(data){
                wait_item2.style.display = 'none';
                if (data.success) {

                    var fileInput = document.getElementById(avatar);
                    var new_avatar = fileInput.files[0];
                    // display the default picture after deleting
                    // am_image is an ID of avatar in the upper half of the page
                    av_image.src = default_avatar_path;
                    document.getElementById("delete_button").disabled = true;
                }
                else {
                }
            },
            error: function (response) {
                wait_item2.style.display = 'none';
                console.log(response.responseText);
            }
        });
        return false;
    });

});