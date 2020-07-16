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
				// var obj = $.extend({}, subjective_questions, subjective_result);
				// console.log(obj);
				// $.each(z, function (i,v) {
				// 		console.log(v.testtype);
				// });
				// console.log(subjective_questions, subjective_result, papers);
				// $.each(papers, function (i,v) {
				// 	console.log(v.testtype);
				// });
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
				let e = 1;
				let c = 1;

				var paper_list = '';
				for (let i =0;i<response.subj_count;i++) {
					paper_list += '<div class="result-list">';
					paper_list += '<table border="0x" class="rl-table">';
					paper_list += '<tr>';
					paper_list += '<td>&nbsp;' + i + '<td>';
					paper_list += '<td>' + response.subj_testname[i] + '<td>';
					paper_list += '<td>Total Questions -' + response.subj_ques_count[i] + ' <td>';
					paper_list += '<td>Paper Date- ' + response.paper_date[i] + '<td>';
					paper_list += '<td><button class="btn-result" style="width: 60px;" class=" btn-subj" onclick="show_ans('+i+')"><span>Show</span></button></td>';
					paper_list += '<td><button class="btn-result" ><span>Evaluate</span></button><td>';
					paper_list += '</tr>';
					paper_list += '</table>';
					paper_list += '<div class="subj-ans" id="subj_'+i+'" style="display: none">';
					paper_list += '<div id="printMe_'+i+'">';
					paper_list += '<table border="2px" style="width:90%; margin-top: 50px;" class="text-center" id="subj_table">';
					paper_list += '<tr>';
					paper_list += '<td colspan="4"><h4 class="text-center text" style="font-weight: 700; margin: 15px auto 10px auto;">Answer Sheet</h4></td>';
					paper_list += '</tr>';
					paper_list += '<tr><td colspan="2">NAME- ' + response.name + '</td><td colspan="2">ROLL NO- ' + response.rollno + '</td></tr>';
					paper_list += '<tr>';
					paper_list += '<th>College- ' + response.college + '</th>';
					paper_list += '<th>Branch- ' + response.branch + '</th>';
					paper_list += '<th>Sem/Sec - ' + response.semester + '/' + response.section + '</th>';
					paper_list += '<th>Sub- ' + response.subj_subject[i] + '</th>';
					paper_list += '</tr>';
					paper_list += '<tr>';
					paper_list += '<th>Marks Obtained-'+response.subj_marks[i] +' </th>';
					paper_list += '<th>Total Que- '+response.subj_ques_count[i]+'</th>';
					paper_list += '<th>Duration- '+response.subj_duration[i]+'</th>';
					paper_list += '<th>Submission Date- '+response.subj_date_posted[i]+'</th>';
					paper_list += '</tr>';
					for(let j =0;j<response.subj_ques_count[i];j++) {
						paper_list += '<tr>';
						paper_list += '<td colspan="4" style="text-align: left; padding:10px 15px 0 15px;">';
						paper_list += ' <div class="que-ans"> <p><b >Question-' + j + '</b>' + ' ' + response.subj_ques[j] + ' <br> <br>';
						paper_list += '<b>Answer- </b>' + response.subj_ans[j] + '  <span></span></p></div></td></tr>';
					}

					paper_list += '</table></div>';
					paper_list += '<h3 style="text-align: center;"> <button class="btn-success btn-print" onclick="printDiv('+i+')">Print</button></h3></div>';
					paper_list += '</div>';
				}
				$('.subj-container').append(paper_list);

				// if(response.subjective) {
				// 	for (let i = 0; i < response.subj_count; i++) {
				// 		$('.subj-container').append(' <div class="result-list">\n' +
				// 			'                <table border="0x" class="rl-table">');
				// 		$('.rl-table').append('<tr><td>&nbsp; ' + e + '</td><td>' + response.subj_testname[i] + '</td><td>Total Questions- ' + response.subj_ques_count + '</td><td>Submission Date- ' + response.subj_date_posted[i] + '</td><td><button class="btn-result" style="width: 60px;" class=" btn-subj" onclick="show_ans()"><span>Show</span></button><td><button class="btn-result" ><span>Evaluate</span></button></td></tr> </table>');
				// 		$('.subj-container').append('<div class="subj-ans" id="subj" ><div id=\'printMe\'><table border="2px" style="width:90%; margin-top: 50px;" class="text-center" id="subj_table">');
				// 		$('#subj_table').append('<tr><td colspan="4"><h4 class="text-center text" style="font-weight: 700; margin: 15px auto 10px auto;">Answer Sheet</h4></td></tr>');
				// 		$('#subj_table').append('<tr><td colspan="2">NAME- ' + response.name + ' </td><td colspan="2">ROLL NO- ' + response.rollno + '</td></tr>');
				// 		$('#subj_table').append('<tr><td>College- ' + response.college + '</td><td>Branch- ' + response.branch + '</td><td>Sem/Sec- ' + response.semester + '/' + response.section + '</td><td>Subject- ' + response.subj_subject[i] + '</td></tr>');
				// 		$('#subj_table').append('<tr><td>Marks Obtained- ' + response.subj_marks + '</td><td>Total Que- ' + response.subj_ques_count + '</td><td>Duration- ' + response.subj_duration + '</td><td>Submission Date- ' + response.subj_date_posted[i] + '</td></tr>');
				//
				// 		for (let j = 0; j < response.subj_ques_count; j++) {
				//
				// 			$('#subj_table').append(' <tr>\n' +
				// 				'                      <td colspan="4" style="text-align: left; padding:10px 15px 0 15px;">\n' +
				// 				'                        <div class="que-ans"> <p><b >Question- ' + c + ' </b>' + response.subj_ques[i] + '<br> <br><b>Answer- ' + response.subj_ans[i] + '</b> <span></span></p></div>\n' +
				// 				'                      </td>\n' +
				// 				'                    </tr>');
				// 			c += 1;
				// 		}
				// 		e += 1;
				// 		$('.subj-container').append('</table>\n' +
				// 			'                </div>\n' +
				// 			'                  <h3 style="text-align: center;"> <button class="btn-success btn-print" onclick="printDiv(\'printMe\')">Print</button></h3>\n' +
				// 			'                </div>\n' +
				// 			'\n' +
				// 			'              </div>');
				// 	}
				// }
				//######################################################################################################################















					// 		$('.subj-container').html(`
					//             <div class="result-list">
					//   <table border="0x" class="rl-table">
					//      <tr><td>&nbsp; 1</td><td>Java Unit-5</td><td>Total Questions- </td><td>Attempted-4</td><td>Submission Date- 13/07/20</td>
					//     <td><button class="btn-result" style="width: 60px;" class=" btn-subj" onclick="show_ans()"><span>Show</span></button>
					//       <td><button class="btn-result" ><span>Evaluate</span></button></td></tr>
					//   </table>
					//   <div class="subj-ans" id="subj" >
					//     <div id='printMe'>
					//
					//     <table border="2px" style="width:90%; margin-top: 50px;" class="text-center" id="subj_table">
					//        <tr><td colspan="4"><h4 class="text-center text" style="font-weight: 700; margin: 15px auto 10px auto;">Answer Sheet</h4></td></tr>
					//       <tr><td colspan="2">NAME- </td><td colspan="2">ROLL NO-</td></tr>
					//       <tr>
					//         <th>College- </th>
					//         <th>Branch- </th>
					//         <th>Sem/Sec - </th>
					//         <th>Sub-</th>
					//       </tr>
					//       <tr>
					//         <th>Marks Obtained- </th>
					//         <th>Total Que-</th>
					//         <th>Duration- </th>
					//         <th>Submission Date- </th>
					//       </tr>
					//      <tr>
					//         <td colspan="4" style="text-align: left; padding:10px 15px 0 15px;">
					//           <div class="que-ans"> <p><b >Question- </b><br> <br>
					//           <b>Answer- </b> <span></span></p></div>
					//         </td>
					//       </tr>
					//           </div>
					//         </td>
					//     </table>
					//   </div>
					//     <h3 style="text-align: center;"> <button class="btn-success btn-print" onclick="printDiv('printMe')">Print</button></h3>
					//   </div>
					// </div>
					// 		`);
				// $('.que-ans').append('<p><b >Question- '+c+'</b>'+response.subj_ques[i]+'<br> <br><b>Answer- '+response.subj_ans[i]+'</b> <span></span></p>')
				// 				c += 1;
					// $('#stu_marks').html(response.marks);
					// $('#stu_name').html(response.name);
					// $('#stu_roll_no').html(response.rollno);
					// $('#stu_semester').html(response.semester);
					// $('#stu_section').html(response.sec);
					// var e = 1;
					// var i;
					// var j = 1;
					// var c = 1;
					// $('#obj_table').append('<tr><th colspan="3">College-'+ response.college +'</th><th colspan="2">Semester- '+response.semester+'th</th><th colspan="2">Section- '+response.sec+'</th></tr>');
					// $('#obj_table').append('<tr><th colspan="3">Name- '+response.name+'</th><th colspan="2">Branch- '+response.branch+'</th><th colspan="2">Roll Number- '+response.rollno+'</th></tr>');
					// $('#obj_table').append('<tr><td>Sr No.</td><td>Test Name</td><td>Subject</td><td>Attempted</td><td>Marks</td><td>Submission Date</td></tr>');
					// for (i = 0; i < count; i++) {
					// 	if (test_type[i]  === 'objective'){
					// 		$('#obj_table').append('<tr><td>'+j+'</td><td>'+response.testname[i]+'</td><td>'+response.subject[i]+'</td><td>'+response.attempted[i]+'</td><td>'+response.marks[i]+'</td><td>'+response.date_posted[i]+'</td></tr>');
					// 	j = j+ 1;
					// 	}
					// 	else{
					// 		$('.rl-table').append( '<tr><td>&nbsp; '+e+'</td><td>'+response.testname[i]+'</td><td>Total Questions- '+response.total_ques[i]+'</td><td>Submission Date- '+response.date_posted[i]+'</td><td><button class="btn-result" style="width: 60px;" class=" btn-subj" onclick="show_ans()"><span>Show</span></button><td><button class="btn-result" ><span>Evaluate</span></button></td></tr>');
					// 		$('#subj_table').append('<tr><td colspan="4"><h4 class="text-center text" style="font-weight: 700; margin: 15px auto 10px auto;">Answer Sheet</h4></td></tr>');
					// 		$('#subj_table').append('<tr><td colspan="2">NAME- '+response.name+' </td><td colspan="2">ROLL NO- '+response.rollno+'</td></tr>');
					// 		$('#subj_table').append('<tr><td>College- '+response.college+'</td><td>Branch- '+response.branch+'</td><td>Sem/Sec- '+response.semester+'/'+response.sec+'</td><td>Subject- '+response.subject[i]+'</td></tr>');
					// 		$('#subj_table').append('<tr><td>Marks Obtained- '+response.marks+'</td><td>Total Que- '+response.total_ques+'</td><td>Duration-</td><td>Submission Date- '+response.date_posted+'</td></tr>');
					// 		e += 1;
					// 	// $('#display_result').append('<tr><td>' + j + '</td><td>' + response.name + '</td><td>' + response.rollno + '</td><td>' + response.semester + '</td><td>' + response.sec + '</td><td>' + response.marks[i] + '</td></tr>');
					// 	$('.que-ans').append('<p><b >Question- '+c+'</b>'+response.question[i]+'<br> <br><b>Answer- '+response.attempted[i]+'</b> <span></span></p>')
					// 	c += 1;
					// }
					// }

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
	});
});