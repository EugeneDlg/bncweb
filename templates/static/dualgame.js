var inputs = ['my_cows', 'my_bulls', 'your_guess'];
function remove_warnings(){
    for (var i=0; i < inputs.length; i++){
        var item = document.getElementById(inputs[i]);
        $(item).removeClass('err_input');
        $('#error_'+item.name).remove();
    };
}
$(document).ready(function () {
    wait_item = document.getElementById('wait');
    wait_item.style.display = 'none';
    $("#game_form").on("submit", function(){
        wait_item.style.display = '';
        if(!game_started){
            return true;
        }
        var dict0 = $(this).serialize();
        var dict_json = dict0 + '&flag=0';
        csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
            url: $(this).data("url"),
            method: 'post',
            dataType: 'json',
            data: dict_json,
            success: function(data){
                remove_warnings();
                if (data.success == false){
                    wait_item.style.display = 'none';
                    tag_items = data.items;
                    for(var key in tag_items) {
                        item = document.getElementById(key);
                        $(item).addClass('err_input');
                        $(item).after('<div class=\'err_label\' id=\'error_' + item.name+ '\'>' + tag_items[key] + '</div>');
                    };
                }
                else {
                    post_dict = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'flag':1};
                    $('body').load('/home/dualgame/', post_dict);
                    $('body').on('load', function() {
                                        wait_item.style.display = 'none';});
                };
            },
            error: function (response) {
                wait_item.style.display = 'none';
                console.log(response.responseJSON.errors);
            }
        });
        return false;
    });
    $("#finish_form").on("submit", function(e){

        var msg = "Are you sure you want to finish the game?";
        if (!confirm(msg)){
            e.preventDefault();
            return false;
        }
        wait_item.style.display = '';
        var dict1 = $(this).serialize();
//        var dict_json1 = dict1 + '&flag=1';

        alert(dd);
        $.ajax({
            url: $("#finish_form").data("url"),
            method: 'post',
            dataType: 'json',
            data: dict1,
            success: function(data){},
            error: function(response){console.log(response);}

        });
    });
    if (game_started){
        var count = 0;
        var f = document.getElementById('my_guess');
        var IntervalId = setInterval(function() {
            if (count++ < 10){
                f.style.fontWeight = (f.style.fontWeight == 'bold' ? 'normal' : 'bold');
            }else{
                clearInterval(IntervalId);
            };
        }, 200);
    };
    wait_item.style.display = 'none';
})