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
    $("#game_form").on("submit", function(){
        wait_item.style.display = '';
        {% if not game.game_started %}
          return true;
        {% endif %}
        var dict_json = $(this).serialize();
//        var dict_json = dict0 + '&flag=0';
        csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        $.ajax({
    	url: '/home/dualgame/',
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
    	    wait_item.style.display = 'none';
//    		post_dict = {'csrfmiddlewaretoken': csrfmiddlewaretoken, 'flag':1};
//    		$('body').load('/home/dualgame/', post_dict);
//    		$('body').on('load', function() {
//    				    wait_item.style.display = 'none';});
    	    };
    	},
    	error: function (response) {
    	      wait_item.style.display = 'none';
    	      console.log(response.responseJSON.errors);
    	}
        });
        return false;
    });
    {% if game.game_started == True %}
    var count = 0;
    var f = document.getElementById('my_guess');
    var IntervalId = setInterval(function() {
      if (count++ < 10){
        f.style.fontWeight = (f.style.fontWeight == 'bold' ? 'normal' : 'bold');
      }else{
        clearInterval(IntervalId);
      };
    }, 200);
    {% endif %}
    wait_item.style.display = 'none';
  })
