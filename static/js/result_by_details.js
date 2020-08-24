$(function(){
	$('#result_btn').click(function(){
		$.ajax({
			url: '/all_details',
			data: $('form').serialize(),
			type: 'POST',
			success: function(data){
				var response = JSON.parse(data);
				var question = response.ques;
				var result = response.result_list;
				var user_details =  response.user;
				console.log(response);

				  var data1 = [];
				  function removeDup(obj, index) {
					if (data1.map(function(e) {
						return e.name;
					  }).indexOf(obj.name) === -1) {
					  data1.push(obj);
					}
				  }
					user_details.filter(removeDup, 0);
				  //starting from here...................................................
				let student_data = '';
				if(response.obj) {
					$('.student-list').remove();
					let c = 1;
                    student_data += '<div class="student-list">';
					student_data += '<div class="result-obj" id="result-obj-details"><table border="2px" style="min-width:700px;">';
					student_data += '<tr style="height: 50px; font-weight: 600;"><td style="width: 10%; padding-left:8px; " >Sr No</td><td style="width: 30%; padding-left:8px;" >Name</td><td style="width: 10%;" class="text-center">Section</td><td style="width: 20%;" class="text-center">Roll Number</td><td style="width: 15%;" class="text-center">Attempted</td><td style="width: 15%;" class="text-center">Marks Obtained</td></tr>';
						for (let i =0;i<result.length;i++) {

							student_data += '<tr><td class="sr-no" style="padding-left:8px;" >'+c+'.</td><td style="padding-left:8px;" >'+data1[i]["name"]+'</td><td class="text-center">'+data1[i]["section"]+'</td><td class="text-center">'+data1[i]["rollno"]+'</td><td class="text-center">' + result[i]["Answer"] + '</td><td class="text-center">' + result[i]["Total_Marks"] + '</td></tr>';

							c += 1;
						}
					student_data += '</table></div>';
					student_data += '</div>';
						$('.results-by-test').append(student_data);
					}
				else {
					let k = 0;
					let h =0;
					let s = 1;
					let index = 1;
					let a = [];
					let sum;
					let count = 0;
					let z = 0;
					function set_marks(){
						for (let i = 0;i<data1.length;i++){
							sum=0;
							for (let j=0;j<question.length;j++){
								sum = sum + parseFloat(result[count]["Total_Marks"]);
								count++;
							}
							a.push(sum);
						}
					}
					set_marks();
					console.log(a);
					$('.student-list').remove();
					for (let i = 0; i < data1.length; i++) {
						student_data += '<div class="student-list">';
						student_data += '<table>';
						student_data += '<tr >';
						student_data += '<td class="sr-no" style="height:40px; padding-left:8px;">'+index+'.</td>';
						student_data += '<td style="width: 27%; padding-left:8px;">' + data1[i]["name"] + '</td><td class="text-center" style="width: 12%;">Section- '+data1[i]["section"]+'</td> <td style="width: 22%;" class="text-center">Roll No:- ' + data1[i]["rollno"] + '</td><td class="text-center" style="width: 12%;">';
						student_data += '<button onclick="toggle_resultbytest('+i+')">Show</button></td>';
						student_data += '<td class="text-center" style="width: 15%;"><button onclick="toggle_evaluate('+i+')" >Evaluate</button></td><td style="width: 12%;" class="text-center"><button onclick="toggle_img('+i+')">Image</button></td></tr>';
						student_data += '</table>';

						//show area

						student_data += '<div id="student_result_div_'+i+'" style="display: none;">';
						student_data += '<div class="result-subj" id="result-subj-details">';
						student_data += '<br><div id="print-res_'+i+'"><table border="2px"><tr id="hidden-details_'+i+'" style="height: 25px;" ><td style="width:50%;padding-left:8px;" >Name- '+data1[i]["name"]+'</td><td colspan="2" class="text-center">Roll No- '+ data1[i]["rollno"] +'</td></tr><tr style="height: 25px;"><td style="width:50%;padding-left:8px;">Testname:- '+response.subj_testname+'</td>';
						student_data += '<td style="width:25%; text-align:center;">Total Ques- '+question.length+'</td><td style="width:25%; text-align:center;">Marks Obtained:- '+a[i]+'</td></tr>';
						for (let j=0;j<question.length;j++) {
							if (user_details[k]["stu_user_id"] === result[k]["User"] ) {
								student_data += '<tr><td colspan="3" style="text-align: left; padding-left: 8px;">Question- '+question[j]["question"]+'<br>';
								student_data += 'Answer:- '+result[k]["Answer"]+'</td> </tr>';
							}
							k += 1;
						}
						student_data += '</table></div></div><div class="text-center"><input type="button" class="btn btn-success submit btn3 rounded-pill"  value="Print" onclick="print_res('+i+')" style="border-radius:2px; height:25px; font-size:15px; padding-top:0;"></div>';
						student_data += '</div>';
						//end show area

						//evaluate area
						student_data += '<div id="student_result_div1_'+i+'" style="display: none;">';
						student_data += '<form action="" role="form">';
						student_data += '<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>';
						student_data += '<input type="hidden" name="id_'+i+'" value="'+data1[i]["stu_user_id"]+'" id="hidden_id_'+i+'">';
						student_data += '<input type="hidden" name="test_id_'+i+'" value="'+result[i]["test_id"]+'" id="testid_'+i+'">';
						student_data += '<input type="hidden" name="result_id_'+i+'" value="'+result[i]["result_id"]+'" id="resultid_'+i+'">';
						student_data += '<input type="hidden" name="question_length'+i+'" value="'+question.length+'" id="question_len'+i+'">';
						student_data += '<div class="result-subj" id="result-subj-details">';
						student_data += '<br><table border="2px" id="table_'+i+'"><tr style="height: 35px; font-weight: 500;"><td style="width:50%;padding-left:8px;">Testname:- '+response.subj_testname+'</td>';
						student_data += '<td class="text-center">Total Ques- '+question.length+'</td><td class="text-center">Marks Obtained:- '+a[i]+'</td></tr>';
						for (let j=0;j<question.length;j++) {
							if (user_details[h]["stu_user_id"] === result[h]["User"] ) {
								student_data += '<tr><td colspan="2" style="text-align: left; padding-left: 8px;width:80%;">Question- '+question[j]["question"]+'<br>';
								student_data += 'Answer:- '+result[h]["Answer"]+'</td><td class="text-center" id="marks_div_'+z+'">Marks Assigned <br> <input type="text" placeholder="'+question[j]["marks_assigned"]+'" disabled><br> <br>Marks Obtained <br> <input type="text" name="marks_obt_'+z+'" id="marks_'+z+'" class="enable_disable_'+i+'" value="'+result[h]["Total_Marks"]+'"> </td></tr>';
								z += 1;
							}
							h += 1;
						}
						//student_data += '</table></div><div class="text-center "><input type="button" id="evaluate_btn_" onclick="evalu('+i+')" class="btn btn-dark btn3 rounded-pill text-center" value="Save"></div></div>';
						//<input type="button" class="btn btn-success submit btn3 rounded-pill"  value="Print Result" onclick="print_res('+i+')"></input>
						student_data += '</table><div class="text-center"><input type="button" class="btn btn-info"  value="Edit" id="edit_btn_'+i+'" onclick="enable_input('+i+')">&nbsp;&nbsp;&nbsp;<input type="button"  onclick="evalu('+i+', '+z+')" class="btn btn-dark text-center" value="Save"></div></div>';
						student_data += '</div>';

						//end evaluate

						//img cap. start
						student_data += '<div id="student_result_div2_'+i+'" style="display: none;" class="res-image">';
						student_data += '<ul>';
						for (let img=1;img<=5;img++) {
							student_data += '<li><img src="/static/student_images/'+response.subj_testname+data1[i]["name"]+img+'.jpg?'+Math.random()+'" id="img_id_'+img+'" onerror="this.src=\'/static/student_images/default.png\';"></li>';
							localStorage.setItem("img"+s, "/static/student_images/"+response.subj_testname+data1[i]["name"]+img+".jpg");
							s += 1;
						}
						student_data += '</ul> <hr class="clr-float"> ';
						student_data += '<h1 class="text-center"><input type="button" class="btn btn-danger"  value="Delete" id="delete_btn_'+i+'" onclick="delete_img('+i+', '+s+')"></h1>';
						student_data += '</form>';
						student_data += '</div>';
						//img cap. end

						student_data += '</div>';
						index += 1;
					}
					$('.results-by-test').append(student_data);
				}

			},
			error: function(error){
				console.log(error);
			}
		});

	});
});
