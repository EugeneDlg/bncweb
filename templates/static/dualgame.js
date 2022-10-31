///*
//Adapted from http://jsfiddle.net/dtrooper/AceJJ/
//
//TODO:
// * Try to get rid of ghosting
// * See if anything can be made more efficient
// * Make the canvas fit in the z-order
//*/
//
//(function( $ ) {
//    var MAX_ROCKETS = 5,
//        MAX_PARTICLES = 500;
//
//    var FUNCTIONS = {
//        'init': function(element) {
//            var jqe = $(element);
//
//            // Check this element isn't already inited
//            if (jqe.data('fireworks_data') !== undefined) {
//                console.log('Looks like this element is already inited!');
//                return;
//            }
//
//            // Setup fireworks on this element
//            var canvas = document.createElement('canvas'),
//                canvas_buffer = document.createElement('canvas'),
//                data = {
//                    'element': element,
//                    'canvas': canvas,
//                    'context': canvas.getContext('2d'),
//                    'canvas_buffer': canvas_buffer,
//                    'context_buffer': canvas_buffer.getContext('2d'),
//                    'particles': [],
//                    'rockets': []
//                };
//
//            // Add & position the canvas
//            if (jqe.css('position') === 'static') {
//                element.style.position = 'relative';
//            }
//            element.appendChild(canvas);
//            canvas.style.position = 'absolute';
//            canvas.style.top = '0px';
//            canvas.style.bottom = '0px';
//            canvas.style.left = '0px';
//            canvas.style.right = '0px';
//
//            // Kickoff the loops
//            data.interval = setInterval(loop.bind(this, data), 1000 / 50);
//
//            // Save the data for later
//            jqe.data('fireworks_data', data);
//        },
//        'destroy': function(element) {
//            var jqe = $(element);
//
//            // Check this element isn't already inited
//            if (jqe.data('fireworks_data') === undefined) {
//                console.log('Looks like this element is not yet inited!');
//                return;
//            }
//            var data = jqe.data('fireworks_data');
//            jqe.removeData('fireworks_data');
//
//            // Stop the interval
//            clearInterval(data.interval);
//
//            // Remove the canvas
//            data.canvas.remove();
//
//            // Reset the elements positioning
//            data.element.style.position = '';
//        }
//    };
//
//    $.fn.fireworks = function(action) {
//        // Assume no action means we want to init
//        if (!action) {
//            action = 'init';
//        }
//
//        // Process each element
//        this.each(function() {
//            FUNCTIONS[action](this);
//        });
//
//        // Chaining ftw :)
//        return this;
//    };
//
//    function launch(data) {
//        if (data.rockets.length < MAX_ROCKETS) {
//            var rocket = new Rocket(data);
//            data.rockets.push(rocket);
//        }
//    }
//
//    function loop(data) {
//        // Launch a new rocket
//        launch(data);
//
//        // Update screen size
//        if (data.canvas_width != data.element.offsetWidth) {
//            data.canvas_width = data.canvas.width = data.canvas_buffer.width = data.element.offsetWidth;
//        }
//        if (data.canvas_height != data.element.offsetHeight) {
//            data.canvas_height = data.canvas.height = data.canvas_buffer.height = data.element.offsetHeight;
//        }
//
//        // Fade the background out slowly
//        data.context_buffer.clearRect(0, 0, data.canvas.width, data.canvas.height);
//        data.context_buffer.globalAlpha = 0.9;
//        data.context_buffer.drawImage(data.canvas, 0, 0);
//        data.context.clearRect(0, 0, data.canvas.width, data.canvas.height);
//        data.context.drawImage(data.canvas_buffer, 0, 0);
//
//        // Update the rockets
//        var existingRockets = [];
//        data.rockets.forEach(function(rocket) {
//            // update and render
//            rocket.update();
//            rocket.render(data.context);
//
//            // random chance of 1% if rockets is above the middle
//            var randomChance = rocket.pos.y < (data.canvas.height * 2 / 3) ? (Math.random() * 100 <= 1) : false;
//
//            /* Explosion rules
//                 - 80% of screen
//                - going down
//                - close to the mouse
//                - 1% chance of random explosion
//            */
//            if (rocket.pos.y < data.canvas.height / 5 || rocket.vel.y >= 0 || randomChance) {
//                rocket.explode(data);
//            } else {
//                existingRockets.push(rocket);
//            }
//        });
//        data.rockets = existingRockets;
//
//        // Update the particles
//        var existingParticles = [];
//        data.particles.forEach(function(particle) {
//            particle.update();
//
//            // render and save particles that can be rendered
//            if (particle.exists()) {
//                particle.render(data.context);
//                existingParticles.push(particle);
//            }
//        });
//        data.particles = existingParticles;
//
//        while (data.particles.length > MAX_PARTICLES) {
//            data.particles.shift();
//        }
//    }
//
//    function Particle(pos) {
//        this.pos = {
//            x: pos ? pos.x : 0,
//            y: pos ? pos.y : 0
//        };
//        this.vel = {
//            x: 0,
//            y: 0
//        };
//        this.shrink = .97;
//        this.size = 2;
//
//        this.resistance = 1;
//        this.gravity = 0;
//
//        this.flick = false;
//
//        this.alpha = 1;
//        this.fade = 0;
//        this.color = 0;
//    }
//
//    Particle.prototype.update = function() {
//        // apply resistance
//        this.vel.x *= this.resistance;
//        this.vel.y *= this.resistance;
//
//        // gravity down
//        this.vel.y += this.gravity;
//
//        // update position based on speed
//        this.pos.x += this.vel.x;
//        this.pos.y += this.vel.y;
//
//        // shrink
//        this.size *= this.shrink;
//
//        // fade out
//        this.alpha -= this.fade;
//    };
//
//    Particle.prototype.render = function(c) {
//        if (!this.exists()) {
//            return;
//        }
//
//        c.save();
//
//        c.globalCompositeOperation = 'lighter';
//
//        var x = this.pos.x,
//            y = this.pos.y,
//            r = this.size / 2;
//
//        var gradient = c.createRadialGradient(x, y, 0.1, x, y, r);
//        gradient.addColorStop(0.1, "rgba(255,255,255," + this.alpha + ")");
//        gradient.addColorStop(0.8, "hsla(" + this.color + ", 100%, 50%, " + this.alpha + ")");
//        gradient.addColorStop(1, "hsla(" + this.color + ", 100%, 50%, 0.1)");
//
//        c.fillStyle = gradient;
//
//        c.beginPath();
//        c.arc(this.pos.x, this.pos.y, this.flick ? Math.random() * this.size : this.size, 0, Math.PI * 2, true);
//        c.closePath();
//        c.fill();
//
//        c.restore();
//    };
//
//    Particle.prototype.exists = function() {
//        return this.alpha >= 0.1 && this.size >= 1;
//    };
//
//    function Rocket(data) {
//        Particle.apply(
//            this,
//            [{
//                x: Math.random() * data.canvas.width * 2 / 3 + data.canvas.width / 6,
//                y: data.canvas.height
//            }]
//        );
//
//        this.explosionColor = Math.floor(Math.random() * 360 / 10) * 10;
//        this.vel.y = Math.random() * -3 - 4;
//        this.vel.x = Math.random() * 6 - 3;
//        this.size = 2;
//        this.shrink = 0.999;
//        this.gravity = 0.01;
//    }
//
//    Rocket.prototype = new Particle();
//    Rocket.prototype.constructor = Rocket;
//
//    Rocket.prototype.explode = function(data) {
//        var count = Math.random() * 10 + 80;
//
//        for (var i = 0; i < count; i++) {
//            var particle = new Particle(this.pos);
//            var angle = Math.random() * Math.PI * 2;
//
//            // emulate 3D effect by using cosine and put more particles in the middle
//            var speed = Math.cos(Math.random() * Math.PI / 2) * 15;
//
//            particle.vel.x = Math.cos(angle) * speed;
//            particle.vel.y = Math.sin(angle) * speed;
//
//            particle.size = 10;
//
//            particle.gravity = 0.2;
//            particle.resistance = 0.92;
//            particle.shrink = Math.random() * 0.05 + 0.93;
//
//            particle.flick = true;
//            particle.color = this.explosionColor;
//
//            data.particles.push(particle);
//        }
//    };
//
//    Rocket.prototype.render = function(c) {
//        if (!this.exists()) {
//            return;
//        }
//
//        c.save();
//
//        c.globalCompositeOperation = 'lighter';
//
//        var x = this.pos.x,
//            y = this.pos.y,
//            r = this.size / 2;
//
//        var gradient = c.createRadialGradient(x, y, 0.1, x, y, r);
//        gradient.addColorStop(0.1, "rgba(255, 255, 255 ," + this.alpha + ")");
//        gradient.addColorStop(0.2, "rgba(255, 180, 0, " + this.alpha + ")");
//
//        c.fillStyle = gradient;
//
//        c.beginPath();
//        c.arc(this.pos.x, this.pos.y, this.flick ? Math.random() * this.size / 2 + this.size / 2 : this.size, 0, Math.PI * 2, true);
//        c.closePath();
//        c.fill();
//
//        c.restore();
//    };
//}(jQuery));

//setTimeout(function() {
//    // $('div').fireworks();
//
//    $('#on_bg').click(function() { $('div.bg').fireworks(); });
//    $('#on_blue').click(function() { $('div.blue').fireworks(); });
//    $('#on_red').click(function() { $('div.red').fireworks(); });
//    $('#on_all').click(function() { $('div').fireworks(); });
//    $('#off_bg').click(function() { $('div.bg').fireworks('destroy'); });
//    $('#off_blue').click(function() { $('div.blue').fireworks('destroy'); });
//    $('#off_red').click(function() { $('div.red').fireworks('destroy'); });
//    $('#off_all').click(function() { $('div').fireworks('destroy'); });
//});

var inputs = ['my_cows', 'my_bulls', 'your_guess'];
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
    show_counter();
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

                if (data.success == false){
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
                    $('body').load('/home/dualgame/', post_dict);
                    $('body').on('load', function() {
                        wait_item.style.display = 'none';
                        ok_button.disabled=false;
                        finished_button.disabled=false;
                    });
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
        ok_button.disabled=true;
        finished_button.disabled=true;
        var dict1 = $(this).serialize();
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
        blink_my_guess();

    }

    if(result_code!=null){
        $('html, body').animate({ scrollTop: 0 }, 'fast');

    }
})
