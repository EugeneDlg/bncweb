var initial_text = "<h2>" + upper_label + "</h2>";
var success_text = initial_text + "<br>" + "<h3>Changes saved <i class=\"material-icons\">done</i></h3>";
var upper_notice = '#upper_notice';
var main_form = "#edit_form";

function initial_text_show(){
     $(upper_notice).html(initial_text);
     $(upper_notice).addClass('initial-upper-notice');
}

$(document).ready(function () {

    initial_text_show();
    $(main_form).on("submit", function(){
        initial_text_show();
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
                    var form_with_button = form_without_button +
                    "<div class=\"justify-content-center  text-center\"><button class=\"btn btn-primary\" type=\"submit\" name=\"button\" >Submit changes</button></div>";
                    $(main_form).html(form_with_button);
                    $('#hint_id_password2').text("");
                }
                else {
                    $(upper_notice).html(success_text);
                }
            },
            error: function (response) {
                console.log(response.responseJSON.errors);
            }
        });
        return false;
    });
});



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
