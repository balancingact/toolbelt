$("body").css("overflow", "hidden");

var prompting = false;
var speed = 0;
var scalar = 35;

$('body').keydown(function(e){
	if(e.keyCode == 32 && prompting){ // Space bar
		console.log("Space");
		if($('html, body').is(':animated')){
			$('html, body').stop();
		} else {
			speed = $('body').html().length * scalar;
			scroll($('html, body'), speed);
		}
	}
	if(e.keyCode == 37 && prompting){ // Left arrow
		console.log("Left");
		$('#prompter').css("font-size", "-=4px");
		$('#prompter').css("line-height", "-=6px");
		$('#fontsize').html($('#fontsize').css('font-size'));
		console.log($('#fontsize').css('font-size'));
		if($('html, body').is(':animated')){
			$('html, body').stop();
			speed = $('body').html().length * scalar;
			scroll($('html, body'), speed);
		}
		$('html, body').stop();
		scroll($('html, body'), speed);
	}
	if(e.keyCode == 38 && prompting && scalar > 1){ // Up arrow
		console.log("Up");
		scalar -= 2;
		$('#speed').html(scalar);
		if($('html, body').is(':animated')){
			$('html, body').stop();
			speed = $('body').html().length * scalar;
			scroll($('html, body'), speed);
		}
	}
	if(e.keyCode == 40 && prompting && scalar < 101){ // Down arrow
		console.log("Down");
		scalar += 2;
		$('#speed').html(scalar);
		if($('html, body').is(':animated')){
			$('html, body').stop();
			speed = $('body').html().length * scalar;
			scroll($('html, body'), speed);
		}
	}
	if(e.keyCode == 39 && prompting){ // Right arrow
		console.log("Right");
		$('#prompter').css("font-size", "+=4px");
		$('#prompter').css("line-height", "+=6px");
		$('#fontsize').html($('#fontsize').css('font-size'));
		console.log($('#fontsize').css('font-size'));
		if($('html, body').is(':animated')){
			$('html, body').stop();
			speed = $('body').html().length * scalar;
			scroll($('html, body'), speed);
		}
	}
});

function onHover() {
	$("#holder").css('border', '10px dashed #888');
	$("#help").css('bottom', '10%');
}

function onLeave() {
	$("#holder").css('border', '10px dashed #ccc');
	$("#help").css('bottom', '-100%');
}

$("#holder").hover(
	onHover, onLeave
)
$("#help").hover(
	onHover, onLeave
)

var onDragOver = function(event) {
    event.preventDefault(); 
    onHover();
};

var onDragLeave = function(event) {
    onLeave()
};

var onDrop = function(event) {
    event.preventDefault();
    var file = event.originalEvent.dataTransfer.files[0],
        reader = new FileReader();
    reader.onload = function(event) {
        loadFile(event.target.result);
    };
    reader.readAsText(file);

    return false;
};

$("#holder").on("dragover", onDragOver).on("dragleave", onDragLeave).on("drop", onDrop);

function loadFile(content){
	$('#speed').html(scalar);
	$('#fontsize').html($('#fontsize').css('font-size'));
    $('body').css('background-color', '#222');
    $('#holder').fadeOut(400, function() { $(this).remove(); });
    $('#help').fadeOut(400, function() { $(this).remove(); });
    $('#prompter').html(content);
    $('#prompter').fadeIn(1000);
    $('#screen').fadeIn(1000);
    $('#howto').delay(700).fadeIn(1000);
	$('#navbar').fadeIn(1000);
	
	prompting = true;
	
	counter = 5;
	var countdown = setInterval(function () { 
		$('#counter').html(counter--);
		if (counter < 0) {
			clearInterval(countdown);
			$('#howto').fadeOut(1000, function() { $(this).remove(); });
			$('#screen').css({
				'background' : '-webkit-linear-gradient(top, rgba(0,0,0,0), rgba(0,0,0,1))',
				'background' : '-o-linear-gradient(bottom, rgba(0,0,0,0), rgba(0,0,0,1))',
				'background' : '-moz-linear-gradient(bottom, rgba(0,0,0,0), rgba(0,0,0,1))',
				'background' : 'linear-gradient(to bottom, rgba(0,0,0,0), rgba(0,0,0,1))',
			});
			$("#screen").delay(800).animate({top: "+=180"}, 800, function() { playPrompter(); });
		}
	}, 1000);
}

function playPrompter() {
	var speed = $('body').html().length * scalar;

	scroll($('html, body'), speed);
}

function scroll(element, speed) {
	element.animate({ scrollTop: $(document).height() }, speed,'linear', function() {
		$(this).animate({ scrollTop: 0 }, speed, scroll(element, speed));
	});
}