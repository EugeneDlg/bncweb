var inputs = ['my_cows', 'my_bulls'];
if (dual_game){
    inputs.push('your_guess');
}
function remove_warnings(){
    for (var i=0; i < inputs.length; i++){
        var item = document.getElementById(inputs[i]);
        $(item).removeClass('err_input');
        $('#error_'+item.name).remove();
    };
}


function blink_my_guess(){
    var count = 0;
    var f = document.getElementById('my_guess');
    var IntervalId = setInterval(function() {
        if (count++ < 12){
            f.style.fontWeight = (f.style.fontWeight == 'bold' ? 'normal' : 'bold');
        }else{
            clearInterval(IntervalId);
        };
    }, 200);
}


function show_counter(){
        var sec_count = elapsed;
        var counter_div = document.getElementById('counter');
        var CounterId = setInterval(function() {
            if (game_started){
                sec_count++;
                var seconds = Math.floor(sec_count % 60);
                var minutes = Math.floor(sec_count / 60) % 60;
                var hours = Math.floor(sec_count / 3600);
                counter_div.innerHTML = "Elapsed: "+ hours +":" + (minutes<10?"0":"") + minutes + ":" + (seconds<10?"0":"") + seconds;
            }
            else{
                clearInterval(CounterId);
                var seconds = Math.floor(sec_count % 60);
                var minutes = Math.floor(sec_count / 60) % 60;
                var hours = Math.floor(sec_count / 3600);
                counter_div.innerHTML = "Elapsed: "+ hours +":" + (minutes<10?"0":"") + minutes + ":" + (seconds<10?"0":"") + seconds;
            }
        }, 1000);
}


$(document).ready(function () {
    wait_item = document.getElementById('wait');
    wait_item.style.display = 'none';
    if(dual_game){
        show_counter();
        var temp = "";
        for (let i=0; i < capacity; i++){temp+="x";}
        alert(temp);
        $("#your_guess").attr('placeholder', temp);
    }
    if(!game_started){
        if (Number(result_code)>0){
                $('#firework_place').fireworks();
        }
    }
    $("#game_form").on("submit", function(){
        wait_item.style.display = '';
        if(!game_started){
            return true;
        }
        ok_button.disabled=true;
        finished_button.disabled=true;
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
                if (!data.success){
                    wait_item.style.display = 'none';
                    ok_button.disabled=false;
                    finished_button.disabled=false;
                    tag_items = data.items;
                    for(var key in tag_items) {
                        item = document.getElementById(key);
                        $(item).addClass('err_input');
                        $(item).after('<div class=\'err_label\' id=\'error_' + item.name+ '\'>' + tag_items[key] + '</div>');
                    };
                }
                else {
                    post_dict = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'flag':1};
                    $('body').load($("#game_form").data("url"), post_dict);
                    $('body').on('load', function() {
                        wait_item.style.display = 'none';
                        ok_button.disabled=false;
                        finished_button.disabled=false;
                    });
                };
            },
            error: function (response) {
                wait_item.style.display = 'none';
                console.log(response.responseText);
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
        ok_button.disabled=true;
        finished_button.disabled=true;
        var dict1 = $(this).serialize();
        $.ajax({
            url: $("#finish_form").data("url"),
            method: 'post',
            dataType: 'json',
            data: dict1,
            success: function(data){},
            error: function(response){console.log(response.responseText);}
        });
    });
    if (game_started){
        blink_my_guess();
    }

    if(result_code!=null){
        $('html, body').animate({ scrollTop: 0 }, 'fast');
    }
})
