//var initial_text = "<h2 >" + "Settings" + "</h2>";
var initial_text = "Settings";
var success_text = initial_text + '<br>' + '<h4 style="color: green;">Changes saved <i class="material-icons">done</i></h4>';
var upper_notice = $('#upper_notice');

function initial_text_show(){
     upper_notice.html(initial_text);
}

$(document).ready(function () {
    initial_text_show();
    $("#settings_form").on("submit", function(){
        initial_text_show();
        $.ajax({
            url: $(this).data("url"),
            method: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(data){
                if (data.success) {
                    upper_notice.html(success_text);
                }
            },
            error: function (response) {
                console.log(response.responseText);
            }
        });
        return false;
    });

});