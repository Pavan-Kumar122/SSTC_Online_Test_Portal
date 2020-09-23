$(function(){
	$('#search_btn').click(function(){
		$.ajax({
			url: '/show_result',
			data: $('form').serialize(),
			type: 'POST',
			success: function(data){
				var response = JSON.parse(data);
				var subjective_result = response.subj_result;
				var subjective_questions = response.subjective_ques;
				var papers = response.all_paper;
				$('#results_by_test').hide();
				$('#obj_table tr').remove();
				if (response.objective){
					$('#obj_table').append('<tr><th colspan="3">College-'+ response.college +'</th><th colspan="2">Semester- '+response.semester+'th</th><th colspan="2">Section- '+response.section+'</th></tr>');
					$('#obj_table').append('<tr><th colspan="3">Name- '+response.name+'</th><th colspan="2">Branch- '+response.branch+'</th><th colspan="2">Roll Number- '+response.rollno+'</th></tr>');
					$('#obj_table').append('<tr><td>Sr No.</td><td>Test Name</td><td>Subject</td><td>Attempted</td><td>Marks</td><td>Submission Date</td></tr>');
					let j = 1;
					for (let i =0; i<response.obj_count;i++){
						$('#obj_table').append('<tr><td>'+j+'</td><td>'+response.obj_testname[i]+'</td><td>'+response.obj_subject[i]+'</td><td>'+response.obj_ans[i]+'</td><td>'+response.obj_marks[i]+'</td><td>'+response.obj_date_posted[i]+'</td></tr>');
						j = j+ 1;
					}
				}
				let sum;
				let a = [];
				let increase=0;
				function set_marks(){
					for (let i = 0;i<response.subj_count;i++){
						sum=0;
						for (let j=0;j<response.subj_ques_count[i];j++){
							sum = sum + parseFloat(response.subj_marks[increase]);
							increase++;
						}
						a.push(sum);
					}
				}
				set_marks();
				let e = 1;
				let c = 0;
				let count = 0;
				let count_1 = 0;
				var paper_list = '';
				let ques_no;
				let ques_no_eval;
				for (let i =0;i<response.subj_count;i++) {
					ques_no = 1;
					ques_no_eval = 1;
					paper_list += '<div class="result-list">';
					paper_list += '<table border="0x" class="rl-table">';
					paper_list += '<tr>';
					paper_list += '<td class="rl-number">' + e + '<td>';
					paper_list += '<td> Testname: ' + response.subj_testname[i] + '<td>';
					paper_list += '<td>Total Questions -' + response.subj_ques_count[i] + ' <td>';
					paper_list += '<td>Paper Date- ' + response.paper_date[i] + '<td>';
					paper_list += '<td><button class="btn-result" style="width: 60px;" class=" btn-subj" onclick="show_ans('+i+')"><span>Show</span></button></td>';
					paper_list += '<td><button class="btn-result" onclick="show_eval('+i+')"><span>Evaluate</span></button><td>';
					paper_list += '</tr>';
					paper_list += '</table>';
					paper_list += '<div class="subj-ans" id="subj_'+i+'" style="display: none">';
					paper_list += '<div id="printMe_'+i+'">';
					paper_list += '<table border="2px" style="width:90%; margin-top: 50px;" class="text-center  rl-table-details" id="subj_table">';
					paper_list += '<tr>';
					paper_list += '<td colspan="4"><h4 class="text-center text" style="font-weight: 700; margin: 15px auto 10px auto;">Answer Sheet</h4></td>';
					paper_list += '</tr>';
					paper_list += '<tr><td colspan="2">NAME- ' + response.name + '</td><td colspan="2">ROLL NO- ' + response.rollno + '</td></tr>';
					paper_list += '<tr>';
					paper_list += '<th>College- ' + response.college + '</th>';
					paper_list += '<th><span class="block-element">Branch-</span> ' + response.branch + '</th>';
					paper_list += '<th>Sem/Sec - ' + response.semester + '/' + response.section + '</th>';
					paper_list += '<th>Sub- ' + response.subj_subject[i] + '</th>';
					paper_list += '</tr>';
					paper_list += '<tr>';
					paper_list += '<th><span class="block-element">Marks Obtained-</span'+a[i] +' </th>';
					paper_list += '<th>Total Que- '+response.subj_ques_count[i]+'</th>';
					paper_list += '<th><span class="block-element">Duration-</span> '+response.subj_duration[i]+'</th>';
					paper_list += '<th>Date Submitted-<br> '+response.subj_date_posted[i]+'</th>';
					paper_list += '</tr>';
					for(let j =0;j<response.subj_ques_count[i];j++) {
						if (count === 0) {
							paper_list += '<tr>';
							paper_list += '<td colspan="4" style="text-align: left; padding:10px 15px 0 15px;">';
							paper_list += ' <div class="que-ans"> <p style="font-weight:500;"><b >Question-' + ques_no + '</b>' + ' ' + response.subj_ques[j] + ' <br> <br>';
							paper_list += '<b>Answer- </b>' + response.subj_ans[j] + '  <span></span></p></div></td></tr>';
						}
						else {
							paper_list += '<tr>';
							paper_list += '<td colspan="4" style="text-align: left; padding:10px 15px 0 15px;">';
							paper_list += ' <div class="que-ans"> <p style="font-weight:500;"><b >Question-' + ques_no + '</b>' + ' ' + response.subj_ques[count] + ' <br> <br>';
							paper_list += '<b>Answer- </b>' + response.subj_ans[count] + '  <span></span></p></div></td></tr>';
						}
						count +=1;
						ques_no += 1;
					}

					paper_list += '</table></div>';
					paper_list += '<h3 style="text-align: center;"> <button class="btn-success btn-print" onclick="printDiv('+i+')">Print</button></h3></div>';

					//evaluate area
					paper_list += '<div class="subj-ans" id="subj1_'+i+'" style="display: none">';
					paper_list += '<form action="" role="form" id="eval_formid_'+i+'">';
					paper_list += '<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>';
					paper_list += '<input type="hidden" name="eval_id_'+i+'" value="'+response.user_id[i]+'" id="eval_hidden_id_'+i+'">';
					paper_list += '<input type="hidden" name="eval_test_id_'+i+'" value="'+response.subj_paper_test_id[i]+'" id="eval_testid_'+i+'">';
					paper_list += '<input type="hidden" name="eval_question_length'+i+'" value="'+response.subj_ques_count[i]+'" id="eval_question_len'+i+'">';
					paper_list += '<table border="2px" style="width:90%; margin-top: 50px;" class="text-center  rl-table-details" id="subj_table">';
					paper_list += '<tr>';
					paper_list += '<td colspan="4"><h4 class="text-center text" style="font-weight: 600; margin: 15px auto 10px auto;">Answer Sheet</h4></td>';
					paper_list += '</tr>';
					paper_list += '<tr><td colspan="2">NAME- ' + response.name + '</td><td colspan="2">ROLL NO- ' + response.rollno + '</td></tr>';
					paper_list += '<tr>';
					paper_list += '<th><span class="block-element">College-</span> ' + response.college + '</th>';
					paper_list += '<th><span class="block-element">Branch-</span> ' + response.branch + '</th>';
					paper_list += '<th>Sem/Sec - ' + response.semester + '/' + response.section + '</th>';
					paper_list += '<th>Sub- ' + response.subj_subject[i] + '</th>';
					paper_list += '</tr>';
					paper_list += '<tr>';
					paper_list += '<th><span class="block-element">Marks Obtained-</span>'+response.subj_marks[i] +' </th>';
					paper_list += '<th>Total Que- '+response.subj_ques_count[i]+'</th>';
					paper_list += '<th>Duration- '+response.subj_duration[i]+'</th>';
					paper_list += '<th>Date Submitted-<br> '+response.subj_date_posted[i]+'</th>';
					paper_list += '</tr>';
					for(let j =0;j<response.subj_ques_count[i];j++) {
						if (count_1 === 0) {
							paper_list += '<tr>';
							paper_list += '<td colspan="3" style="text-align: left; padding:10px 15px 0 15px;">';
							paper_list += ' <div class="que-ans"> <p style="font-weight:500;"><b >Question-' + ques_no_eval + '</b>' + ' ' + response.subj_ques[j] + ' <br> <br>';
							paper_list += '<b>Answer- </b>' + response.subj_ans[j] + '  <span></span></p></div></td><td id="eval_marks_div_'+c+'" style="min-width:170px;">Marks Assigned <br> <input type="text" placeholder="'+response.marks_asign[j]+'" disabled> <br>Marks Obtained <br> <input type="text" name="eval_marks_obt_'+c+'" id="eval_marks_'+c+'" class="eval_enable_disable_'+i+'" value="'+response.subj_marks[j]+'"> </td></tr>';
							c += 1;
						}
						else {
							paper_list += '<tr>';
							paper_list += '<td colspan="3" style="text-align: left; padding:10px 15px 0 15px;">';
							paper_list += ' <div class="que-ans"> <p style="font-weight:500;"><b>Question-' + ques_no_eval + '</b>' + ' ' + response.subj_ques[count_1] + ' <br> <br>';
							paper_list += '<b>Answer- </b>' + response.subj_ans[count_1] + '  <span></span></p></div></td><td id="eval_marks_div_'+c+'">Marks Assigned <br> <input type="text" placeholder="'+response.marks_asign[j]+'" disabled> <br>Marks Obtained <br> <input type="text" name="eval_marks_obt_'+c+'" id="eval_marks_'+c+'" class="eval_enable_disable_'+i+'" value="'+response.subj_marks[j]+'"> </td></tr>';
							c += 1;
						}
						count_1 +=1;
						ques_no_eval += 1;
					}

					paper_list += '</table>';
					paper_list += '<h3 style="text-align: center;margin-top: 5px;"> <input type="button" class="btn btn-info"  value="Edit" id="edit_btn_'+i+'" onclick="eval_enable_input('+i+')">&nbsp;&nbsp;&nbsp;<input type="button"  onclick="eval_evalu('+i+', '+c+')" class="btn btn-dark text-center" value="Save"></h3></div></div>';
					paper_list += '</form>';

					//end evaluate
					paper_list += '</div>';
					e += 1;
				}
				$('.subj-container').append(paper_list);

			},
			error: function(error){
				console.log(error);
				// setTimeout(function(){
       			//
    			// 	}, 5000);
				$('#error').empty();
				$('#show-results').hide();
				$('#error').show();
				$('#error').append('Please Enter a valid User Id');
				$('#error').hide(8000);
			}
		});
				$('.result-list').remove();

	});
});
