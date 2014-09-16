$(document).ready(function(){
	var cheat_activated = true;
	$(".poster").hover(function(){
		$(".img_overlay").toggleClass("hidden");
	});

	$("#reveal_plot").click(function(){
		$("#entire_plot").show();
		$("#reveal_plot").hide();
	});


	$(window).blur(function(){
		// setInterval(function(){alert(window.location.href)}, 3000);
		if (cheat_activated == false){

			var game = $("#game_id").val();
			cheat_activated = true;
			vex.dialog.open({
				message: "Oh, we went to another tab, did we? <br> Maybe we went to rottentomatoes.com, hmmm? <br>NO POINTS FOR ANYONE!",
				overlayClosesOnClick: false,
				buttons: [
					$.extend({}, vex.dialog.buttons.YES, {
	      				text: 'Start new round. Cheater.'})
				],
				callback: function(){
					
						window.location.href = "/next_round?game_id=" + game; 
					
				}

			});
		}
	});


});