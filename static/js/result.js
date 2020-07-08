$(function(){
	$('#search_btn').click(function(){
		$.ajax({
			url: '/show_result',
			data: $('form').serialize(),
			type: 'POST',
			success: function(data){
				var response = JSON.parse(data);
				var count = response.count;
					// $('#stu_marks').html(response.marks);
					// $('#stu_name').html(response.name);
					// $('#stu_roll_no').html(response.rollno);
					// $('#stu_semester').html(response.semester);
					// $('#stu_section').html(response.sec);
				var i;
				var j = 1;
				for (i = 0; i < count; i++) {
					  	// $('#stu_marks').html(response.marks);
						// $('#stu_name').html(response.name);
						// $('#stu_roll_no').html(response.rollno);
						// $('#stu_semester').html(response.semester);
						// $('#stu_section').html(response.sec);
						$('#display_result').append('<tr><td>' + j + '</td><td>' + response.name + '</td><td>' + response.rollno + '</td><td>' + response.semester + '</td><td>' + response.sec + '</td><td>' + response.marks[i] + '</td></tr>');
						j = j+ 1;
					}

			},
			error: function(error){
				console.log(error);
			}
		});
	});
});