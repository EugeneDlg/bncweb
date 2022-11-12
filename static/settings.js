//var initial_text = "<h2 >" + "Settings" + "</h2>";
var initial_text = "Settings";
var success_text = initial_text + '<br>' + '<h4 style="color: green;">Changes saved <i class="material-icons">done</i></h4>';
var upper_notice = $('#upper_notice');

function initial_text_show(){
     upper_notice.html(initial_text);
}

$(document).ready(function () {
    wait_item = document.getElementById('wait');
    wait_item.style.display = 'none';
    initial_text_show();
    $("#settings_form").on("submit", function(){
        wait_item.style.display = '';
        initial_text_show();
        $.ajax({
            url: $(this).data("url"),
            method: 'post',
            dataType: 'json',
            data: $(this).serialize(),
            success: function(data){
                wait_item.style.display = 'none';
                if (data.success) {
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

});