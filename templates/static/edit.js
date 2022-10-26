var initial_text = "<h2>" + upper_label + "</h2>";
var success_text = initial_text + "<br>" + "<h3>Changes saved <i class=\"material-icons\">done</i></h3>";
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
        var reader = new FileReader();
//            reader.onload = function(e) {
//                document.getElementById(
//                    'imagePreview').innerHTML =
//                    '<img src="' + e.target.result
//                    + '"/>';
//            };
        reader.readAsDataURL(fileInput.files[0]);
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
     upper_notice.attr("style", "color: green; font-weight: bold;");
}

function setImageVisible(id, visible) {
    var img = document.getElementById(id);
    img.style.visibility = (visible ? 'visible' : 'hidden');
}

$(document).ready(function () {
    document.getElementById("delete_button").disabled = !is_avatar_available;
    initial_text_show();

    $(main_form).on("submit", function(){
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
                if (!(data.success)) {
                var form_without_button = data['form_html'].replace(/<form .*?>/, "");
                form_without_button = form_without_button.replace(/<\/form>/, "");
                var form_with_button = form_without_button + "<button class=\"form_auth_button\" type=\"submit\" name=\"button\" >Submit changes</button>";
                $(this).html(form_with_button);
                $('#hint_id_password2').text("");
                $(div_avatar).addClass("file_attention");
                }
                else {
                    var fileInput = document.getElementById(avatar);
                    if (fileInput.files && fileInput.files[0]) {
                        av_image.src = URL.createObjectURL(fileInput.files[0]);
                        document.getElementById("delete_button").disabled = false;
                    }
                    upper_notice.html(success_text);
                }
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            }
        });
        return false;
    });

    $("#delete_av_form").on("submit", function(){
        $.ajax({
            url: $(this).data("url"),
            method: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(data){
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
                console.log(response.responseJSON.errors);
            }
        });
        return false;
    });

});

//var initial_text = "<h2>" + upper_label + "</h2>";
//var success_text = initial_text + "<br>" + "<h3>Changes saved <i class=\"material-icons\">done</i></h3>";
//
//
//$(document).ready(function () {
//    var upper_notice = $('#upper_notice');
////    upper_notice.text(initial_text);
//    upper_notice.html(initial_text);
//    upper_notice.attr("style", "color: green; font-weight: bold;");
//$("#edit_form").on("submit", function(){
//    upper_notice.html(initial_text);
//$.ajax({
//    url: $("#edit_form").data("url"),
//    dataType: 'json',
//    method: 'post',
//    data: $(this).serialize(),
//    success: function(data) {
//        if (!(data.success)) {
//    	var form_without_button = data['form_html'].replace(/<form .*?>/, "");
//    	form_without_button = form_without_button.replace(/<\/form>/, "");
//    	var form_with_button = form_without_button + "<button class=\"edit_button\" type=\"submit\" name=\"button\" >Submit changes</button>";
//    	console.log(form_with_button);
//        $('#edit_form').html(form_with_button);
//        $('#hint_id_password2').text("");
//        }
//        else {
//            // Here you can show the user a success message or do whatever you need
//            //$('#signup_form').find('.success-message').show();
////            success_item.style.display = '';
////            initial_notice.style.display = 'none';
////            var url = window.location.href;
////            var pattern = /(.*\/{2})(.*?\/)(.*)/i;
////            var result = url.match(pattern);
//            upper_notice.html(success_text);
//
//        }
//    },
//    error: function (response) {
//        console.log(response.responseJSON.errors);
//    }
//});
//return false;
//});
//
//});
