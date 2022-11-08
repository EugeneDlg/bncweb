//var initial_text = "<h2 >" + "Settings" + "</h2>";
//var initial_text = "Settings";
//var success_text = initial_text + '<br>' + '<h4 style="color: green;">Changes saved <i class="material-icons">done</i></h4>';
//var upper_notice = $('#upper_notice');
//
//function initial_text_show(){
//     upper_notice.html(initial_text);
//}
function show_my_number(){
var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
var dict0 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
dict0 = dict0 + "&f=1";

            $.ajax({
            url: '/about/',
            method: 'post',
            dataType: 'json',
            data: dict0,
            success: function(data){
                    alert("My number is " + data.my_number);
            },
            error: function (response) {
                console.log(response.responseText);
            }
        });
        return false;
}
$(document).ready(function () {

//    document.getElementById("invis").style.display="none";
//    $("#settings_form").on("submit", function(){
//        initial_text_show();
//        $.ajax({
//            url: $(this).data("url"),
//            method: 'post',
//            dataType: 'json',
//            data: $(this).serialize(),
//            success: function(data){
//                if (data.success) {
//                    upper_notice.html(success_text);
//                }
//            },
//            error: function (response) {
//                console.log(response.responseJSON.errors);
//            }
//        });
//        return false;
//    });

});