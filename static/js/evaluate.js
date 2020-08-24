$(function(){
	let i =0;
	$('#evaluate_btn_').click(function(){
		$.ajax({
			url: '/evaluate',
			data: $('form').serialize(),
			type: 'POST',
			success: function(data){
				var response = JSON.parse(data);
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});

	});
});
