
	$(document).ready(function(){



		$(document.body).on("click", "#another_movie", function(){
			$.ajax({
				type: "POST",
				url: '/game',
				data: {},
				success: function(result){
					$('#game_content').html(result);

				}
			});
		});



		$(document.body).on("click", "#reveal_ratings", function(){
			$('#ratings').show();
			$("#reveal_ratings").hide();
		});

		$(document.body).on('click', "#reveal_plot", function(){
			$("#entire_plot").show();
			$("#reveal_plot").hide();
		});


		// $("#actor_entered").text = "Nicolas Cage";
		// $("#players").text = "Larry, Curly, Moe";

		// $("#start_game").click(function(){
		// 	var actor_entered = $("#actor_entered").val();
		// 	var players = $("#players").val();

		// 	$.ajax({
		// 		type: "POST",
		// 		url: "/game_test",
		// 		data: {actor_entered: actor_entered,
		// 				players: players},
		// 		success: function(data){
		// 			$('html').html(data);
		// 		}
		// 	});
		// });

		$("#players").keydown(function(){
			if($("#actor_entered").val().length > 0 && $("#players").val().length > 0){
				$("#start_game").removeAttr('disabled');
			};
		});

		$("#actor_entered").keydown(function(){
			if ($("#players").val().length > 0 && $("#actor_entered").val().length > 0){
				$("#start_game").removeAttr('disabled');
			};
		});

		// $("#start_game").click(function(){
		// 	$.ajax({
		// 		type: 'POST',
		// 		url: '/',
		// 		data: {actorName: value.actor},
		// 		success: function(result){
		// 				$('#game_content').html(result);

		// });
	


		// vex.dialog.open({
		// 	message: "Which actor/actress are we searching for?",
		// 	overlayClosesOnClick: false,
		// 	input: "<input name=\'actor\' id='actor_vex' placeholder='Which actor?' required  autofocus/>",
		// 	buttons: [
		//         // $.extend({}, vex.dialog.buttons.YES, text: 'Login')
		//         $.extend({}, vex.dialog.buttons.YES, {text: "OK"}),
		//         $.extend({}, vex.dialog.buttons.NO, {text: 'Surprise me!', click: function(){
		//         	var random_actors = ['Tom Cruise', "Nicolas Cage", "Angelina Jolie", "Chuck Norris", "Meryl Streep"];
		// 			var actor_list_length = random_actors.length;
		// 			var rand_index = Math.floor((Math.random()* actor_list_length));
		// 			var chosen_actor = random_actors[rand_index];
		// 			$('#actor_vex').val(chosen_actor);
		//         }
		//     })

		//     ],


		// 	callback: function(value){
		// 		// var actor_input = value;
		// 		// console.log(actor_input);
		// 		$.ajax({
		// 		type: 'POST',
		// 		url: '/',
		// 		data: {actorName: value.actor},
		// 		success: function(result){
		// 				$('#game_content').html(result);
		// 			}
		// 		});

		// 	}


		// });



		// vex.dialog.open({

		// 	message: "How many players?",
		// 	input: "<input name=\'num_of_players\' type='text' default='1' />",
		// 	callback: function(value){


		// 		var entered_num = parseInt(value.num_of_players);
		// 		var input_html = '';
		// 		for(i=1; i <= entered_num; i++){
		// 			input_html.append("<input name=\'Player" + String(i) + "\' placeholder='Player"+ String(i)+ "'/>");

		// 		};
		// 		vex.dialog.open({
		// 			message: "What are the player names?",
		// 			console.log(input_html)
		// 			input: input_html,
		// 		});

		// 	}
		// });

		// $('#num_players').hide();
		// $('#enter_player_num').hide();


		//only start game if there is at least one player and one actor defined
		function enable_start_button(){
			if($('#player1').val() != '' && $('#actor').val() != ''){
				$('#start_game').removeAttr('disabled');
			}else{
				$('#start_game').attr('disabled', true);
			};
		};


		//print out actor name on page
		// $('#actor').focusout(function(){
		// 	var actor_name = $('#actor').val();
		// 	var actor_entry = actor_name + "<br><br><br>";
		// 	$('#print_actor').html(actor_entry);
			
		// });
		// $('#actor').keyup(function(){
		// 	enable_start_button();
		// });


		// $('#player1').change(function(){
		// 	enable_start_button();
		// });

		$('#random_actor').click(function(){
			var random_actors = ['Tom Cruise', "Nicolas Cage", "Angelina Jolie", "Chuck Norris", "Meryl Streep"];
			var actor_list_length = random_actors.length;
			var rand_index = Math.floor((Math.random()* actor_list_length));
			var chosen_actor = random_actors[rand_index];
			alert(chosen_actor);
		});

		//show input fields necessary for additonal players
		// $('#moreplayers').click(function(){
		// 	$('#enter_player_num').toggle();
		// 	$('#num_players').toggle();

		// });


		//Create additonal inputs for more players
		$('#num_players').keyup(function(){
			var player_num = parseInt($('#num_players').val());
			$('#more_players').html('')
			if(player_num){
				for(var i=2; i < player_num + 1; i++ ){
					console.log(i);
					var player_html ="<input name='player" + String(i) + "' id='player" + String(i) + "' placeholder='Enter name of player " + String(i) + "'></br>";
					$(player_html).appendTo('#more_players');
					console.log(player_html);
				};
			};
		});


		//print out number of players
		// $('#print_now').click(function(){
		// 	$('#playerInfo').html('');
		// 	var number_players = $('.players input').length;
		// 	var player_list = [];

		// 	for(var i=1; i <= number_players; i++){
		// 		var player_ID = "#player" + String(i);
		// 		var player_name = String($(player_ID).val());
		// 		//exclude empty fields
		// 		if(player_name){
		// 			player_list.push(player_name);
		// 		};
		// 	};
		// 	//print out player names
		// 	for(x=0; x < player_list.length; x++){
		// 		var player_entry = "Player " + String(x + 1) + ": " + player_list[x] + "<br>";
		// 		$('#playerInfo').append(player_entry);	
		// 	}; 
		// 		// console.log(player_entry);
		// 		// $((playerName).val()).appendTo('#playerInfo');	
			
		// 	// $("#playerInfo").html(player_info);
		// });

		//get imdb info through tornado request handler
		$('#get_entered_actor').click(function(){
			var actor_name = $('#actor').val();
			$('#python_response').text('')
			$.ajax({
				type: 'GET',
				url: '/getactor',
				data: {actorName: actor_name},
				success: function(result){
					$('#python_response').text(result);
				}
				});
		});


		//Randomly choose an actor/actress
		$('#surprise').click(function(){
			var random_actors = ['Tom Cruise', "Nicolas Cage", "Angelina Jolie", "Chuck Norris", "Meryl Streep"];
			var actor_list_length = random_actors.length;
			var rand_index = Math.floor((Math.random()* actor_list_length));
			var chosen_actor = random_actors[rand_index];
			$('#actor').val(chosen_actor);
		});

		// $('#print_entered_actor').click(function(){
		// 	var entered_actor = $('#actor').val();
		// 	if (entered_actor){
		// 		$('#print_actor').text(entered_actor);
		// 	}else{
		// 		$('#print_actor').text("Please enter an actor's name.");
		// 	};

		// });

		// $('#start_game').click(function(){

		// 	$.get('/game');
		// });

	});