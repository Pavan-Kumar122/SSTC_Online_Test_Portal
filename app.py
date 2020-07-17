import os
import re
from datetime import datetime, date, timedelta
from dateutil import parser
from flask import Flask, render_template, redirect, request, url_for, flash, json, session
from flask_assets import Bundle, Environment
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_mail import Mail, Message
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
csrf = CSRFProtect(app)
assets = Environment(app)
css = Bundle('css/Fstyle.css', output='ques/main.css')
assets.register('main_css', css)

app.config['SECRET_KEY'] = b"\x07\x92\xde\xa5%YP\xf6\xd2\xb4\xad\x13," \
                           b"\x7f\x949\x89?'A\xb0\x9ep\x0f\x8b=\xfe\xef\x93\xf7:i\xe6\xba<_Y(" \
                           b"\xebe\xf6o\x90'\xc3?\x9f\x0c\x93\xad[" \
                           b"\xf3\xb9\xc4\x95\xce\xc18\x87*m\xd3\x805\xcf\xf7\xf0\xcf\x91\xf9]\xc7\xc5$<\xe0O\x8cx" \
                           b"\x84\x99\xd8" \
                           b"\x8eqF*G\xa6i[H\xb3Yp\xa0\xa6QB\xeebt\xc7\xd7\xb1\xbe{" \
                           b"D\xb1%\xa6e!\xd56\xd7\x8aZ2\x8aPD\xa1\xf3\x12\\\x16\xa2\x85 "

app.permanent_session_lifetime = timedelta(hours=5)
app.config["MYSQL_HOST"] = os.environ.get('MYSQL_HOST')
app.config["MYSQL_USER"] = os.environ.get('MYSQL_USER')
app.config["MYSQL_PASSWORD"] = os.environ.get('MYSQL_PASSWORD')
app.config["MYSQL_DB"] = os.environ.get('MYSQL_DB')
DATABASE_URL = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('Email_ADD')
app.config['MAIL_PASSWORD'] = 'equiqhpzpegsdnzl'
app.static_folder = 'static'
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message_category = 'danger'

name = ""
description = ""
college = ""
branch = ""
semester = ""
section = ""
subject = ""
total_ques = ""
test_type = ""
duration = 0
scheduled_date = ""
hour = ""
minute = ""
sem = ""
sec = ""
st_time = ""
en_time = ""
correct = 0
wrong = 0
attempt = 0
sub_ans = []
time = ""
check = False


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    userid = db.Column(db.Integer, unique=True, nullable=False)
    rollno = db.Column(db.Integer)
    email = db.Column(db.String(80), unique=True, nullable=False)
    branch = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    semester = db.Column(db.String(10))
    college = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(50))
    role = db.Column(db.String(50))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # papers = db.relationship('Paperdetails', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=300):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"Users('{self.role}','{self.username}', '{self.userid}', '{self.rollno}', '{self.email}'," \
               f" '{self.branch}', '{self.semester}', '{self.college}', '{self.image_file}') "


class Paperdetails(db.Model, UserMixin):
    test_id = db.Column(db.Integer, primary_key=True)
    testname = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    semester = db.Column(db.String(50))
    section = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    totalques = db.Column(db.Integer, nullable=False)
    totaltime = db.Column(db.String(50), nullable=False)
    testtype = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, nullable=False)
    scheduled_date = db.Column(db.String(60))
    start_time = db.Column(db.String(60), nullable=False)
    end_time = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Paperdetails('{self.testname}','{self.college}','{self.branch}','{self.testtype}','{self.section}','{self.subject}','{self.start_time}','{self.end_time}','{self.test_id}','{self.scheduled_date}','{self.semester}','{self.totaltime}','{self.description}'," \
               f" {self.date_posted}) "


class Questions(db.Model, UserMixin):
    ques_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(900), nullable=False)
    op1 = db.Column(db.String(100))
    op2 = db.Column(db.String(100))
    op3 = db.Column(db.String(100))
    op4 = db.Column(db.String(100))
    obj_ans = db.Column(db.String(50))
    ques_no = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Questions('{self.question}','{self.ques_id}','{self.test_id}','{self.ques_no}','{self.user_id}','{self.op1}', '{self.op2}', '{self.op3}', '{self.op4}'," \
               f" '{self.obj_ans}') "


class Result(db.Model, UserMixin):
    result_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    testtype = db.Column(db.String(900), nullable=False)
    attempted = db.Column(db.String(100))
    correct = db.Column(db.String(100))
    total_marks = db.Column(db.String(100))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    test_given = db.Column(db.String(20))

    def __repr__(self):
        return f"Result('{self.result_id}','{self.test_id}','{self.test_given}','{self.user_id}','{self.testtype}', '{self.attempted}', '{self.correct}', '{self.total_marks}'," \
               f" '{self.date_posted}') "


class QuestionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Questions

    ques_id = ma.auto_field()
    test_id = ma.auto_field()
    user_id = ma.auto_field()
    question = ma.auto_field()
    op1 = ma.auto_field()
    op2 = ma.auto_field()
    op3 = ma.auto_field()
    op4 = ma.auto_field()
    obj_ans = ma.auto_field()
    ques_no = ma.auto_field()


class ResultSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Result

    result_id = ma.auto_field()
    test_id = ma.auto_field()
    user_id = ma.auto_field()
    testtype = ma.auto_field()
    attempted = ma.auto_field()
    correct = ma.auto_field()
    total_marks = ma.auto_field()
    date_posted = ma.auto_field()
    test_given = ma.auto_field()


class PaperSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Paperdetails

    test_id = ma.auto_field()
    testname = ma.auto_field()
    description = ma.auto_field()
    college = ma.auto_field()
    branch = ma.auto_field()
    semester = ma.auto_field()
    section = ma.auto_field()
    subject = ma.auto_field()
    totalques = ma.auto_field()
    totaltime = ma.auto_field()
    testtype = ma.auto_field()
    date_posted = ma.auto_field()
    user_id = ma.auto_field()
    scheduled_date = ma.auto_field()
    start_time = ma.auto_field()
    end_time = ma.auto_field()


def validate_username(username):
    user = Users.query.filter_by(username=username).first()
    return user


def validate_email(email):
    vemail = Users.query.filter_by(email=email).first()
    return vemail


def validate_reset_email(email):
    VRemail = Users.query.filter_by(email=email).first()
    return VRemail
    # if it is none raise email is not registered.


def validate_user_id(user_id):
    vuser_id = Users.query.filter_by(userid=user_id).first()
    return vuser_id


def findid(user_id):
    if user_id[0] == '3035' or user_id[0] == '3014' or user_id[0] == '3036':
        return 1
    else:
        return 0


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        if current_user.role == 'Student':
            return redirect(url_for('student_login'))
        else:
            return redirect(url_for('faculty_login'))
    if request.method == 'POST':
        user = Users.query.filter_by(userid=request.form['Lid']).first()
        if user is None:
            flash("Please check Email and Password", 'danger')
            return render_template('index.html')
        else:
            get_role = user.role
            if get_role == 'Student':
                if user and bcrypt.check_password_hash(user.password, request.form['Lpassword']):
                    remember_me = request.form.get('remember')
                    if remember_me is None:
                        login_user(user)
                        return redirect(url_for('student_login'))
                    else:
                        login_user(user, remember=remember_me)
                        return redirect(url_for('student_login'))
                else:
                    flash("Please check Email and Password", 'danger')
            else:
                if user and bcrypt.check_password_hash(user.password, request.form['Lpassword']):
                    remember_me = request.form.get('remember')
                    if remember_me is None:
                        login_user(user)
                        return redirect(url_for('faculty_login'))
                    else:
                        login_user(user, remember=remember_me)
                        return redirect(url_for('faculty_login'))
                else:
                    flash("Please check Email and Password", 'danger')
    return render_template('index.html')


@app.route('/registerData', methods=['GET', 'POST'])
def registerData():
    if current_user.is_authenticated:
        if current_user.role == 'Student':
            return redirect(url_for('student_login'))
        else:
            return redirect(url_for('faculty_login'))
    if request.method == 'POST':
        error = ""
        if request.form.get("id", "") == "1":
            hashed_password = bcrypt.generate_password_hash(request.form['Spassword']).decode('utf-8')
            vusername = validate_username(username=request.form['Sname'])
            vemail = validate_email(email=request.form['Semail'])
            vuserid = validate_user_id(user_id=request.form['Sid'])
            if vusername is None:
                if vemail is None:
                    if vuserid is None:
                        user_id = request.form['Sid']
                        match = re.findall(r'(\d{4})', str(user_id))
                        Vid = findid(match)
                        if Vid == 1:
                            if len(str(user_id)) == 12:
                                user = Users(username=request.form['Sname'], userid=request.form['Sid'],
                                             rollno=request.form['Srollno'],
                                             email=request.form['Semail'], branch=request.form['Sbranch'],
                                             semester=request.form['Ssemester'], college=request.form['Scollege'],
                                             section=request.form['Ssection'], password=hashed_password, role='Student')
                                db.session.add(user)
                                db.session.commit()
                                flash("Account Created! Please Log In", 'success')
                                return redirect(url_for('index'))
                            else:
                                error = 'User Id must be of 12 Digits!!'
                        else:
                            error = 'Please Enter a Valid User Id !!'
                    else:
                        error = "User Id is Already Taken!"
                else:
                    error = "Email is Already Taken!"
            else:
                error = "Username Already Taken!!"
            return render_template('register.html', error=error)
        else:
            hashed_password = bcrypt.generate_password_hash(request.form['Fpassword']).decode('utf-8')
            vusername = validate_username(username=request.form['Fname'])
            vemail = validate_email(email=request.form['Femail'])
            vuserid = validate_user_id(user_id=request.form['Fid'])
            if vusername is None:
                if vemail is None:
                    if vuserid is None:
                        user = Users(username=request.form['Fname'], userid=request.form['Fid'],
                                     email=request.form['Femail'], branch=request.form['Fbranch'],
                                     college=request.form['Fcollege'],
                                     password=hashed_password, role='Faculty')
                        db.session.add(user)
                        db.session.commit()
                        flash("Account Created! Please Log In", 'success')
                        return redirect(url_for('index'))
                    else:
                        error = "User Id is Already Taken!"
                else:
                    error = "Email is Already Taken!"
            else:
                error = "Username Already Taken!!"
            return render_template('register.html', error=error)
    return redirect(url_for('register'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/student/main', methods=['GET', 'POST'])
@login_required
def student_login():
    global time_limit, get_ques, paper, e, set_test_id, time, check
    get_ques = ""
    time_limit = ""
    paper1 = ""
    get_paper = Paperdetails.query.filter(Paperdetails.semester.contains(current_user.semester),
                                          Paperdetails.section.contains(current_user.section),
                                          Paperdetails.scheduled_date.like(date.today()),
                                          Paperdetails.college.like(current_user.college),
                                          Paperdetails.branch.like(current_user.branch)).all()
    # print(get_paper)
    sub_ans = []
    correct = 0
    wrong = 0
    attempt = 0
    set_test_id = ""
    if get_paper:
        for i in get_paper:
            if i.start_time <= str(datetime.now().time()) < i.end_time:
                res = Result.query.filter(Result.test_id.contains(i.test_id),
                                          Result.user_id.contains(current_user.id)).all()
                if res:
                    check = False
                    flash('You have Given the test Thank You!!', 'primary')
                    return render_template('student/student_login.html', check=check)
                else:
                    time = i.totaltime
                    time_limit = i.totaltime
                    if int(time) > 3600:
                        time = "{0}Hour:{1}minute".format(int(int(time) / 3600), int((int(int(time) % 3600)) / 60))
                    else:
                        time = "{0}Hour:{1}minute".format(0, int(int(time) / 60))
                    get_ques = Questions.query.filter(Questions.test_id.like(i.test_id))
                    set_test_id = i.test_id
                    paper1 = Paperdetails.query.filter(Paperdetails.test_id.like(i.test_id))
                    check = True
        session['test_id'] = set_test_id
        print(set_test_id)
        if not paper1:
            flash("No New Paper Uploaded!!", 'info')
            return render_template('student/student_login.html', check=False)
        else:

            return render_template('student/student_login.html', get_ques=get_ques,
                                   time_limit=time_limit, time=time, check=check, paper1=paper1)
    else:
        flash("No New Paper Uploaded!!", 'info')
        return render_template('student/student_login.html', check=False)


@app.route('/showresult', methods=['GET', 'POST'])
def showresult():
    global time_limit, get_ques, paper, e, set_test_id, correct, wrong, time, check, sub_ans
    if 'test_id' in session:
        test_id = session['test_id']
        session.permanent = True
        get_ques = Questions.query.filter(Questions.test_id.like(test_id))
        print(get_ques)
    if request.method == 'POST':
        sub_ans = []
        for ques in get_ques:
            if request.form.get('objective') == 'objective':
                obj_ans = Questions.query.filter_by(ques_id=request.form.get('id_' + str(ques.ques_id)))
                user_ans = request.form.get('Obj_option_' + str(ques.ques_no))
                get_test_id = ques.test_id
                for result in obj_ans:
                    if result.obj_ans == user_ans:
                        correct += 1
                    else:
                        wrong += 1
            else:
                get_test_id = ques.test_id
                sub_ans.append(request.form.get('subj_' + str(ques.ques_no)))
        if request.form.get('objective') == 'objective':
            obj_result = Result(test_id=get_test_id, user_id=current_user.id, testtype='objective',
                                attempted=str(correct + wrong), correct=correct, total_marks=correct,
                                date_posted=datetime.now(), test_given='Yes')
            db.session.add(obj_result)
            db.session.commit()
        else:
            for i in range(0, len(sub_ans)):
                if sub_ans[i] == "":
                    sub_ans[i] = 'Not Attempted'
                subj_result = Result(test_id=get_test_id, user_id=current_user.id, testtype='subjective',
                                     attempted=sub_ans[i], date_posted=datetime.now(), test_given='Yes')
                db.session.add(subj_result)
                db.session.commit()
    print(sub_ans)
    flash('Thank You!!', 'primary')
    return render_template('student/show_result.html')


@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    return render_template('student/exam.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('student/profile_new.html')


@app.route('/faculty/main', methods=['GET', 'POST'])
@login_required
def faculty_login():
    global post
    time = ""
    ques = Questions.query.filter_by(user_id=current_user.id).all()
    faculty_post = Paperdetails.query.filter_by(user_id=current_user.id)
    for f in faculty_post:
        time = f.totaltime
        if int(time) > 3600:
            f.totaltime = "{0}Hour:{1}minute".format(int(int(time) / 3600), int((int(int(time) % 3600)) / 60))
        else:
            f.totaltime = "{0}Hour:{1}minute".format(0, int(int(time) / 60))
    check = False
    for i in faculty_post:
        check = True
    if not check:
        flash("You Haven't Uploaded Any Paper!!", 'danger')
        return render_template('faculty/faculty_home.html', check=check)
    else:
        return render_template('faculty/faculty_home.html', post=faculty_post, ques=ques)


@app.route('/paper_data', methods=['GET', 'POST'])
@login_required
def paper_data():
    global name, description, college, section, semester, subject, branch, total_ques, test_type, scheduled_date, hour, minute, sem, sec, duration, st_time, en_time
    sem = []
    sec = []
    duration = 0
    if request.method == 'POST':
        name = request.form['testname']
        description = request.form['description']
        college = request.form['college']
        semester = request.form.getlist('ques_semester')
        subject = request.form['subject']
        branch = request.form['branch']
        section = request.form.getlist('ques_section')
        total_ques = request.form['total_ques']
        test_type = request.form['test_type']
        scheduled_date = request.form.get('date')
        hour = request.form['hour']
        minute = request.form['minute']
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        st_time = parser.parse(start_time)
        en_time = parser.parse(end_time)
        st_time = str(st_time.time())
        en_time = str(en_time.time())
        # print("{0}Hour:{1}minute".format(hour, minute))
        # i = "{0}Hour:{1}minute".format(hour, minute)
        # print(i)
        duration = int(((int(hour) * 60) + int(minute)) * 60)
        # print(duration)
        # print(name, description, college, semester, subject, branch,
        #       section, total_ques, test_type, date, hour, minute)
        for sem1 in semester:
            sem.append(sem1)
        for sec1 in section:
            sec.append(sec1)
        semester = str(sem)[1:-1].replace("'",
                                          "").replace(",", "")
        # print(semester)
        section = str(sec)[1:-1].replace("'",
                                         "").replace(",", "")
        if not section:
            section = str('A B C D')
        print(section)
        # semester = str(sem)[1:-1].replace("'",
        #                                   "").replace(",", "").replace(" ", "")
        # section = str(sec)[1:-1].replace("'",
        #                                  "").replace(",", "").replace(" ", "")
        # for element in range(0, len(section)):
        #     print(section[element])
        if test_type == 'objective':
            # print(int(total_ques))
            return render_template('faculty/add_ques.html', ques=int(total_ques), branch=branch, semester=semester,
                                   section=section, subject=subject, testname=name, description=description,
                                   test_type=test_type, college=college)
        else:
            return render_template('faculty/add_ques_subjective.html', ques=int(total_ques), branch=branch,
                                   semester=semester,
                                   section=section, subject=subject, testname=name, description=description,
                                   test_type=test_type, college=college)
    return redirect(url_for('faculty_login'))


@app.route('/add_ques', methods=['GET', 'POST'])
@login_required
def add_ques():
    global name, description, semester, total_ques, test_type, college, branch, section, subject, duration, scheduled_date, st_time, en_time
    if request.method == 'POST':
        if request.form.get("obj", "") == "1":
            test_details = Paperdetails(testname=name, description=description, college=college, branch=branch,
                                        semester=semester,
                                        section=section, subject=subject, totalques=total_ques, totaltime=duration,
                                        testtype=test_type, user_id=current_user.id, scheduled_date=scheduled_date,
                                        start_time=st_time, end_time=en_time)
            db.session.add(test_details)
            db.session.commit()
            # current_test_id = Paperdetails.query.filter_by(test_id=current_user.id).first()
            max = db.session.query(db.func.max(Paperdetails.test_id)).first()
            total_ques = int(total_ques)
            for i in range(1, total_ques + 1):
                ques = Questions(test_id=max[-1], user_id=current_user.id, question=request.form['ques_' + str(i)],
                                 op1=request.form['op1_' + str(i)], op2=request.form['op2_' + str(i)],
                                 op3=request.form['op3_' + str(i)], op4=request.form['op4_' + str(i)],
                                 obj_ans=request.form['obj_ans_' + str(i)], ques_no=i)
                db.session.add(ques)
                db.session.commit()
        else:
            test_details = Paperdetails(testname=name, description=description, college=college, branch=branch,
                                        semester=semester,
                                        section=section, subject=subject, totalques=total_ques, totaltime=duration,
                                        testtype=test_type, user_id=current_user.id, scheduled_date=scheduled_date,
                                        start_time=st_time, end_time=en_time)
            db.session.add(test_details)
            db.session.commit()
            # current_test_id = Paperdetails.query.filter_by(test_id=current_user.id).first()
            max = db.session.query(db.func.max(Paperdetails.test_id)).first()
            total_ques = int(total_ques)
            for i in range(1, total_ques + 1):
                ques = Questions(test_id=max[-1], user_id=current_user.id,
                                 question=request.form['ques_' + str(i)], ques_no=i)
                db.session.add(ques)
                db.session.commit()
    return redirect(url_for('paper_data'))


@app.route('/show_result', methods=['POST'])
def show_result():
    global stu_id, stu_marks, stu_section, stu_semester, stu_name, stu_college, stu_branch,\
        subj_testname, obj_testname, subj_subject, subj_stu_marks, subj_ques, obj_type, obj_ans,\
        subj_ans, subj_date_posted, subj_duration, subj_type, obj_duration, obj_date_posted, obj_stu_marks,\
        obj_subject, subj, obj, total_ques_subj, p, all_papers, obj_result, subj_result, subj_q, duration, subj_paper_date_posted, subj_paper_test_id

    p = []
    student_id = request.form['student_id']
    get_user = Users.query.filter(Users.userid.contains(student_id)).all()
    if not get_user:
        return json.dumps({'Please enter a valid User Id !'})
    else:
        for id in get_user:
            stu_id = id.id
            stu_name = id.username
            stu_semester = id.semester
            stu_section = id.section
            stu_college = id.college
            stu_branch = id.branch
        result = Result.query.filter(Result.user_id.contains(stu_id)).all()
        if not result:
            # flash('This User did not given any test', 'danger')
            return
        else:
            all_papers = []
            obj_ans = []
            total_ques_obj = ''
            obj_subject = []
            obj_testname = []
            obj_ques = []
            total_ques_subj = []
            subj_subject = []
            subj_testname = []
            subj_ques = []
            test_id = []
            subj_stu_marks = []
            obj_stu_marks = []
            obj_date_posted = []
            subj_date_posted = []
            subj_ans = []
            obj_result = []
            subj_result = []
            subj_q = []
            duration = []
            subj_paper_date_posted = []
            subj_paper_test_id = []
            for res in result:
                test_id.append(res.test_id)
            test_id = list(dict.fromkeys(test_id))
            obj_type = 0
            subj_type = 0
            for r in range(0, len(test_id)):
                papers = Paperdetails.query.filter(Paperdetails.test_id.contains(test_id[r])).all()
                for p in papers:
                    all_papers.append(p)
                    if p.testtype == 'objective':
                        obj = 'objective'
                        obj_type += 1
                        obj_res = Result.query.filter(Result.test_id.contains(p.test_id)).all()
                        for r in obj_res:
                            obj_result.append(r)
                            obj_ans.append(r.attempted)
                            obj_stu_marks.append(r.total_marks)
                            obj_date_posted.append(r.date_posted)
                        total_ques_obj = p.totalques
                        obj_duration = p.totaltime
                        if int(obj_duration) > 3600:
                            obj_duration = "{0}Hour:{1}minute".format(int(int(obj_duration) / 3600),
                                                                      int((int(int(obj_duration) % 3600)) / 60))
                        else:
                            obj_duration = "{0}Hour:{1}minute".format(0, int(int(obj_duration) / 60))
                        obj_subject.append(p.subject)
                        obj_testname.append(p.testname)
                    else:
                        subj_paper_test_id.append(p.test_id)
                        subj_paper_date_posted.append(p.date_posted)
                        subj = 'subjective'
                        subj_type += 1
                        subj_res = Result.query.filter(Result.test_id.contains(p.test_id)).all()
                        # print(subj_res)
                        for r in subj_res:
                            subj_result.append(r)
                            subj_ans.append(r.attempted)
                            subj_stu_marks.append(r.total_marks)
                            subj_date_posted.append(r.date_posted)
                        total_ques_subj.append(p.totalques)
                        subj_duration = p.totaltime
                        if int(subj_duration) > 3600:
                            subj_duration = "{0}Hour:{1}minute".format(int(int(subj_duration) / 3600),
                                                                       int((int(int(subj_duration) % 3600)) / 60))
                        else:
                            subj_duration = "{0}Hour:{1}minute".format(0, int(int(subj_duration) / 60))
                        duration.append(subj_duration)
                        subj_subject.append(p.subject)
                        subj_testname.append(p.testname)
                        s_question = Questions.query.filter(Questions.test_id.contains(p.test_id)).all()
                        for q in s_question:
                            subj_ques.append(q.question)
                            subj_q.append(q)
    print(subj_paper_test_id)
    # print(subj_result)
    # print(subj_ques)
    paper_schema = PaperSchema(many=True)
    all_paper = paper_schema.dumps(all_papers)
    all_paper_op = paper_schema.loads(all_paper)
    # print(all_paper_op)
    ques_schema = QuestionSchema(many=True)
    subj_question = ques_schema.dumps(subj_q)
    subj_question_op = ques_schema.loads(subj_question)
    result_schema = ResultSchema(many=True)
    subj_results = result_schema.dumps(subj_result)
    subj_result_op = result_schema.loads(subj_results)
    # ques = Questions.query.filter(Questions.test_id.like(1))
    # schema = QuestionSchema(many=True)
    # ques_output = schema.dumps(ques)
    # ques_get = schema.loads(ques_output)
    # print(p)
    # print(subj_type)
    # print(obj_type)
    stu_roll_no = student_id
    return json.dumps(
        {'status': 'OK', 'name': stu_name, 'college': stu_college, 'branch': stu_branch,
         'semester': stu_semester, 'section': stu_section, 'rollno': stu_roll_no,
         'obj_testname': obj_testname, 'subj_testname': subj_testname, 'obj_subject': obj_subject,
         'subj_subject': subj_subject, 'obj_ans': obj_ans, 'subj_ans': subj_ans, 'obj_marks': obj_stu_marks,
         'subj_marks': subj_stu_marks, 'subj_date_posted': subj_date_posted, 'obj_date_posted': obj_date_posted,
         'subj_ques': subj_ques, 'subj_duration': duration, 'obj_duration': obj_duration,
         'obj_count': obj_type, 'subj_count': subj_type, 'subjective': subj, 'objective': obj,
         'subj_ques_count': total_ques_subj, 'subj_result': subj_result_op, 'subjective_ques': subj_question_op,
         'all_paper': all_paper_op, "paper_date": subj_paper_date_posted})


@app.route('/register')
def register():
    if current_user.is_authenticated:
        if current_user.role == 'Student':
            return redirect(url_for('student_login'))
        else:
            return redirect(url_for('faculty_login'))
    return render_template('register.html')


@app.route('/student')
def student():
    return render_template('student_register.html')


@app.route('/pre_exam')
def pre_exam():
    return render_template('student/pre-exam_new.html')


@app.route('/faculty')
def faculty():
    return render_template('faculty_register.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
    msg.body = f'''To reset your password, please visit the following link:
{url_for('newpassword', token=token, _external=True)}

If you did not make this request then simply ignore this Email.
Thank You.
'''
    mail.send(msg)


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    if request.method == 'POST':
        user = Users.query.filter_by(email=request.form['Remail']).first()
        if user is None:
            flash('This Email is not registered yet! Please use a valid email!!', 'danger')
            return redirect(url_for('index'))
        else:
            send_reset_email(user)
            flash('An email has been sent to your registered Email Id !', 'info')
            return redirect(url_for('index'))
    return render_template('forget_password.html')


@app.route('/newpassword/<token>', methods=['GET', 'POST'])
def newpassword(token):
    user = Users.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", 'warning')
        return redirect(url_for('resetpassword'))
    if request.method == 'POST':
        hashed_pwd = bcrypt.generate_password_hash(request.form['New_Password'])
        user.password = hashed_pwd
        db.session.commit()
        flash('The Password has been Successfully Change! Please Log In')
        return redirect(url_for('index'))
    return render_template('new_password.html')


if __name__ == '__main__':
    app.run()
