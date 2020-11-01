import os
import re
import collections
from datetime import datetime, date, timedelta
from dateutil import parser
from flask import Flask, render_template, redirect, request, url_for, flash, json, session, jsonify
from flask_assets import Bundle, Environment
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import base64

app = Flask(__name__)
csrf = CSRFProtect(app)
assets = Environment(app)
css = Bundle('css/Fstyle.css', output='ques/main.css')
assets.register('main_css', css)
ALLOWED_IMAGE_EXTENSIONS = {'jpeg', 'png', 'jpg'}

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
# DATABASE_URL = 'sqlite:///data.db'
DATABASE_URL = 'mysql://root:P@van122@localhost/otp'
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('Email_ADD')
app.config['MAIL_PASSWORD'] = 'equiqhpzpegsdnzl'
app.config['WTF_CSRF_TIME_LIMIT'] = None
app.static_folder = 'static'
db = SQLAlchemy(app)
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
c_ans = ''
w_ans = ''


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    userid = db.Column(db.BIGINT, unique=True, nullable=False)
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
        return f"Users('{self.role}','{self.username}', '{self.userid}', '{self.rollno}','{self.id}', '{self.email}'," \
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
    totalques = db.Column(db.String(80), nullable=False)
    totaltime = db.Column(db.String(50), nullable=False)
    testtype = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, nullable=False)
    scheduled_date = db.Column(db.String(60))
    start_time = db.Column(db.String(60), nullable=False)
    end_time = db.Column(db.String(60), nullable=False)
    correct_ans = db.Column(db.Integer, default=1)
    wrong_ans = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Paperdetails('{self.testname}','{self.college}','{self.branch}','{self.testtype}','{self.section}','{self.subject}','{self.start_time}','{self.end_time}','{self.test_id}','{self.scheduled_date}','{self.semester}','{self.totaltime}','{self.description}'," \
               f" {self.date_posted},{self.correct_ans}, {self.wrong_ans} ) "


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
    marks_assign = db.Column(db.String(60))

    def __repr__(self):
        return f"Questions('{self.question}','{self.ques_id}','{self.test_id}','{self.ques_no}','{self.user_id}','{self.op1}', '{self.op2}', '{self.op3}', '{self.op4}'," \
               f" '{self.obj_ans}', {self.marks_assign}) "


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
        return f"Result('{self.result_id}','{self.test_id}','{self.test_given}','{self.user_id}','{self.testtype}', '{self.attempted}', '{self.correct}', '{self.total_marks}','{self.date_posted}') "


class image_data(db.Model, UserMixin):
    img_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.TEXT)
    user_id = db.Column(db.Integer)
    test_id = db.Column(db.Integer)

    def __repr__(self):
        return f"image_data('{self.img_id}','{self.image}','{self.user_id}','{self.test_id}') "


class SaveFeedBack(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    feedback = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, default=datetime.now())


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
    try:
        if user_id[0] == '3035' or user_id[0] == '3014' or user_id[0] == '3036':
            return 1
        else:
            return 0
    except:
        return 0


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


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
            flash("Please check User Id and Password", 'danger')
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
                    flash("Please check User Id and Password", 'danger')
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
                    flash("Please check User Id and Password", 'danger')
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
            Fid = request.form['Fid']
            if len(str(Fid)) == 6:
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
            else:
                error = 'Please enter a valid User Id'
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
    if request.method == 'POST':
        if request.form.get('hide') == '1':
            s = request.form['stud_profile_name']
            return 'hello student'
        return 'got it'
    global time_limit, get_ques, paper, e, set_test_id, time, check, c_ans, w_ans
    get_ques = ""
    time_limit = ""
    paper1 = ""
    get_paper = Paperdetails.query.filter(Paperdetails.semester.contains(current_user.semester),
                                          Paperdetails.section.contains(current_user.section),
                                          Paperdetails.scheduled_date.like(date.today()),
                                          Paperdetails.college.like(current_user.college),
                                          Paperdetails.branch.like(current_user.branch)).all()

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
                        time = "{0}Hour:{1}mins".format(int(int(time) / 3600), int((int(int(time) % 3600)) / 60))
                    else:
                        time = "{0}mins".format(int(int(time) / 60))
                    get_ques = Questions.query.filter(Questions.test_id.like(i.test_id))
                    set_test_id = i.test_id
                    paper1 = Paperdetails.query.filter(Paperdetails.test_id.like(i.test_id))
                    for s in paper1:
                        c_ans = s.correct_ans
                        w_ans = s.wrong_ans
                    check = True
            else:
                if str(datetime.now().time()) < i.start_time:
                    flash(f'Upcoming Paper {i.testname} on {i.start_time}', 'primary')
                    return render_template('student/student_login.html', check=False)
        session['test_id'] = set_test_id
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
    global time_limit, get_ques, paper, e, set_test_id, correct, wrong, time, check, sub_ans, c_ans, w_ans
    if 'test_id' in session:
        test_id = session['test_id']
        session.permanent = True
        get_ques = Questions.query.filter(Questions.test_id.like(test_id))
    if request.method == 'POST':
        sub_ans = []
        quesno = 0
        correct = 0
        wrong = 0
        attempted = 0
        mark_obt = 0
        for ques in get_ques:
            if request.form.get('objective') == 'objective':
                objective_ans = Questions.query.filter_by(ques_id=request.form.get('id_' + str(ques.ques_id)))
                user_ans = request.form.get('Obj_option_' + str(ques.ques_no))
                if user_ans is not None:
                    attempted = attempted + 1
                get_test_id = ques.test_id
                for result in objective_ans:
                    quesno += 1
                    if result.obj_ans == user_ans:
                        correct += 1
                        mark_obt += c_ans
                    else:
                        mark_obt = mark_obt - w_ans
            else:
                get_test_id = ques.test_id
                sub_ans.append(request.form.get('subj_' + str(ques.ques_no)))
        if request.form.get('objective') == 'objective':
            obj_result = Result(test_id=get_test_id, user_id=current_user.id, testtype='objective',
                                attempted=attempted, correct=correct, total_marks=mark_obt,
                                date_posted=datetime.now(), test_given='Yes')
            db.session.add(obj_result)
            db.session.commit()
            return render_template('student/redirect.html', attempt=attempted, correct=correct,
                                   marks=mark_obt, outof=quesno)
        else:
            for i in range(0, len(sub_ans)):
                if sub_ans[i] == "":
                    sub_ans[i] = 'Not Attempted'
                subj_result = Result(test_id=get_test_id, user_id=current_user.id, testtype='subjective',
                                     attempted=sub_ans[i], date_posted=datetime.now(), test_given='Yes')
                db.session.add(subj_result)
                db.session.commit()
            return redirect(url_for('student_login'))


@app.route('/exam', methods=['GET', 'POST'])
@login_required
def exam():
    return render_template('student/exam.html')


@app.route('/stu_feedback', methods=['GET', 'POST'])
@login_required
def stu_feedback():
    return render_template('student/student_feedback.html')


@app.route('/stud_prof_up', methods=['POST'])
def stud_prof_up():
    current_user.userid = request.form['stu_csvtuid']
    current_user.email = request.form['stu_email']
    current_user.username = request.form['stu_username']
    current_user.college = request.form['stu_college']
    current_user.branch = request.form['stu_branch']
    current_user.semester = request.form['stu_semester']
    current_user.section = request.form['stu_section']
    db.session.commit()
    flash('Updated Successfully', 'primary')
    return redirect(url_for('student_login'))


@app.route('/faculty/main', methods=['GET', 'POST'])
@login_required
def faculty_login():
    global post
    if request.method == 'POST':
        if request.form.get('paper_delete', "") == '1':
            data = request.form['paper_id']
            delete_paper = Paperdetails.query.get(data)
            delete_ques = Questions.query.filter_by(test_id=data).all()
            for d in delete_ques:
                Questions.query.filter_by(test_id=d.test_id).delete()
                Result.query.filter_by(test_id=d.test_id).delete()
            db.session.delete(delete_paper)
            db.session.commit()
    ques = Questions.query.filter_by(user_id=current_user.id).all()
    faculty_post = Paperdetails.query.filter_by(user_id=current_user.id)
    for f in faculty_post:
        time = f.totaltime
        if int(time) > 3600:
            f.totaltime = "{0}Hour:{1}min".format(int(int(time) / 3600), int((int(int(time) % 3600)) / 60))
        else:
            f.totaltime = "{0}Hour:{1}min".format(0, int(int(time) / 60))
    check = False
    for i in faculty_post:
        check = True
    if not check:
        error = "You Haven't Uploaded Any Paper!!"
        return render_template('faculty/faculty_home.html', check=check, error=error)
    else:
        return render_template('faculty/faculty_home.html', post=faculty_post, ques=ques)


@app.route('/faculty_update', methods=['POST', 'GET'])
def faculty_update():
    fname = validate_username(username=request.form['fac_username'])
    fuserid = validate_user_id(user_id=request.form['fac_userid'])
    femail = validate_email(email=request.form['fac_email'])
    up = 0
    if len(str(request.form['fac_userid'])) == 6:
        if fname is None:
            current_user.username = request.form['fac_username']
            up += 1
        if femail is None:
            current_user.email = request.form['fac_email']
            up += 1
        if fuserid is None:
            current_user.userid = request.form['fac_userid']
            up += 1
        current_user.college = request.form['fac_college']
        current_user.branch = request.form['fac_branch']
        up += 1
        db.session.commit()
    else:
        flash('Please enter a digit UserId!', 'danger')
    if up >= 1:
        flash('Profile updated successfully', 'info')
    # current_user.username = request.form['fac_username']
    # current_user.college = request.form['fac_college']
    # current_user.branch = request.form['fac_branch']
    # current_user.userid = request.form['fac_userid']
    # current_user.email = request.form['fac_email']
    # db.session.commit()
    return redirect(url_for('faculty_login'))


@app.route('/feedback', methods=['POST', 'GET'])
def Feedback():
    feed = request.form['feedback']
    if feed == '':
        return json.dumps(dict(empty='yes'))
    else:
        set_feed = SaveFeedBack(username=current_user.username, feedback=feed, date_posted=datetime.now())
        db.session.add(set_feed)
        db.session.commit()
        return json.dumps(dict(status='Right'))


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
        duration = int(((int(hour) * 60) + int(minute)) * 60)
        for sem1 in semester:
            sem.append(sem1)
        for sec1 in section:
            sec.append(sec1)
        semester = str(sem)[1:-1].replace("'",
                                          "").replace(",", "")
        section = str(sec)[1:-1].replace("'",
                                         "").replace(",", "")
        if not section:
            section = str('A B C D')
        if test_type == 'objective':
            # print(int(total_ques))
            return render_template('faculty/add_ques.html', ques=int(total_ques), branch=branch, semester=semester,
                                   section=section, subject=subject, testname=name, description=description,
                                   test_type=test_type, college=college, scheduled_date=scheduled_date)
        else:
            return render_template('faculty/add_ques_subjective.html', ques=int(total_ques), branch=branch,
                                   semester=semester,
                                   section=section, subject=subject, testname=name, description=description,
                                   test_type=test_type, college=college, scheduled_date=scheduled_date)
    return redirect(url_for('faculty_login'))


@app.route('/add_ques', methods=['GET', 'POST'])
@login_required
def add_ques():
    global name, description, semester, total_ques, test_type, college, branch, section, subject, duration, scheduled_date, st_time, en_time
    if request.method == 'POST':
        if request.form.get("obj", "") == "1":
            correct_ans = request.form['correct_answer']
            wrong_ans = request.form['minus_mark']
            test_details = Paperdetails(testname=name, description=description, college=college, branch=branch,
                                        semester=semester,
                                        section=section, subject=subject, totalques=total_ques, totaltime=duration,
                                        testtype=test_type, user_id=current_user.id, scheduled_date=scheduled_date,
                                        start_time=st_time, end_time=en_time, date_posted=datetime.now(),
                                        correct_ans=correct_ans, wrong_ans=wrong_ans)
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
                                        start_time=st_time, end_time=en_time, date_posted=datetime.now())
            db.session.add(test_details)
            db.session.commit()
            # current_test_id = Paperdetails.query.filter_by(test_id=current_user.id).first()
            max = db.session.query(db.func.max(Paperdetails.test_id)).first()
            total_ques = int(total_ques)
            for i in range(1, total_ques + 1):
                ques = Questions(test_id=max[-1], user_id=current_user.id,
                                 question=request.form['ques_' + str(i)], ques_no=i,
                                 marks_assign=request.form['marks_assign_' + str(i)])
                db.session.add(ques)
                db.session.commit()
    return redirect(url_for('paper_data'))


def json_serial(obj1):
    if isinstance(obj1, (datetime, date)):
        return obj1.isoformat()
    raise TypeError("Type %s not serializable" % type(obj1))


@app.route('/show_result', methods=['POST'])
def show_result():
    global stu_id, stu_marks, stu_section, stu_semester, stu_name, stu_college, stu_branch, \
        subj_testname, obj_testname, subj_subject, subj_stu_marks, subj_ques, obj_type, obj_ans, \
        subj_ans, subj_date_posted, subj_duration, subj_type, obj_duration, obj_date_posted, obj_stu_marks, \
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
        s_id = stu_id
        result = Result.query.filter(Result.user_id.contains(stu_id)).all()
        if not result:
            return json.dumps({'No Results Found'})
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
            obj = ""
            obj_duration = ''
            subj = " "
            user_id = []
            marks_asign = []
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
                        obj_res = Result.query.filter(Result.test_id.contains(p.test_id),
                                                      Result.user_id.contains(s_id)).all()
                        for r in obj_res:
                            obj_result.append(r)
                            obj_ans.append(r.attempted)
                            obj_stu_marks.append(r.total_marks)
                            obj_date_posted.append(r.date_posted)
                        total_ques_obj = p.totalques
                        obj_duration = p.totaltime
                        if int(obj_duration) > 3600:
                            obj_duration = f"{int(int(obj_duration) / 3600)}Hour:{int((int(int(obj_duration) % 3600)) / 60)}minute"
                        else:
                            obj_duration = f"{0}Hour:{int(int(obj_duration) / 60)}minute"
                        obj_subject.append(p.subject)
                        obj_testname.append(p.testname)
                    else:
                        subj_paper_test_id.append(p.test_id)
                        subj_paper_date_posted.append(p.date_posted)
                        subj = 'subjective'
                        subj_type += 1
                        subj_res = Result.query.filter(Result.test_id.contains(p.test_id),
                                                       Result.user_id.contains(s_id)).all()
                        # print(subj_res)
                        for r in subj_res:
                            user_id.append(r.user_id)
                            subj_result.append(r)
                            subj_ans.append(r.attempted)
                            subj_stu_marks.append(r.total_marks)
                            subj_date_posted.append(r.date_posted.strftime('%a-%Y-%m-%d'))
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
                            marks_asign.append(q.marks_assign)
                            subj_ques.append(q.question)
                            subj_q.append(q)
    stu_roll_no = student_id
    user_id = list(dict.fromkeys(user_id))
    # print(obj_stu_marks)
    return json.dumps(
        dict(status='OK', name=stu_name, college=stu_college, branch=stu_branch, semester=stu_semester,
             section=stu_section, rollno=stu_roll_no, obj_testname=obj_testname, subj_testname=subj_testname,
             obj_subject=obj_subject, subj_subject=subj_subject, obj_ans=obj_ans, subj_ans=subj_ans,
             obj_marks=obj_stu_marks, subj_marks=subj_stu_marks, subj_date_posted=subj_date_posted,
             obj_date_posted=obj_date_posted, subj_ques=subj_ques, subj_duration=duration, obj_duration=obj_duration,
             obj_count=obj_type, subj_count=subj_type, subjective=subj, objective=obj, subj_ques_count=total_ques_subj,
             paper_date=subj_paper_date_posted, user_id=user_id
             , subj_paper_test_id=subj_paper_test_id, marks_asign=marks_asign), default=json_serial)


@app.route('/all_details', methods=['POST', 'GET'])
def all_details():
    get_test_id = request.form['Rtest']
    # testpaper = Paperdetails.query.filter_by(test_id=get_test_id).all()
    testname = db.session.execute(f'call get_test_name({get_test_id})')
    obj = ""
    subj = ''
    obj_testname = ''
    subj_testname = ''
    d = ''
    a = ''
    c = ''
    stu_user_id = 0
    for t in testname:
        if t == 'objective':
            obj = 'objective'
            obj_testname = t.__str__().strip('()').strip(',').replace("'", "")
        else:
            subj = 'subjective'
            subj_testname = t.__str__().strip('()').strip(',').replace("'", "")
    # ques = Questions.query.filter_by(test_id=get_test_id).all()
    ques = db.session.execute(f'call get_ques_details({get_test_id})')
    objects_list = []
    for row in ques:
        d = collections.OrderedDict()
        d['id'] = row.__getitem__('test_id')
        d['User id'] = row.__getitem__('user_id')
        d['Question'] = row.__getitem__('ques_no')
        d['question'] = row.__getitem__('question')
        d['marks_assigned'] = row.marks_assign
        objects_list.append(d)
    # result = Result.query.filter_by(test_id=get_test_id).all()
    result = db.session.execute(f'call get_result({get_test_id})')
    result_list = []
    user_details = []
    for r in result:
        a = collections.OrderedDict()
        a['Sr No'] = r.result_id
        a['User'] = r.user_id
        a['Test-type'] = r.testtype
        a['Answer'] = r.attempted
        a['Total_Marks'] = r.total_marks
        a['Date_Posted'] = r.date_posted
        a['test_id'] = r.test_id
        a['result_id'] = r.result_id
        result_list.append(a)
        u = Users.query.get(r.user_id)
        c = collections.OrderedDict()
        c['rollno'] = u.userid
        c['name'] = u.username
        c['stu_user_id'] = u.id
        c['section'] = u.section
        c['semester'] = u.semester
        user_details.append(c)
    # get_image = image_data.query.filter_by(test_id=get_test_id).all()
    get_image = db.session.execute(f'call get_image({get_test_id})')
    image_details = []
    image_stu_id = []

    for img in get_image:
        image = collections.OrderedDict()
        image['image_data'] = img.image
        image['id'] = img.img_id
        image['user_id'] = img.user_id
        image_stu_id.append(img.user_id)
        image_details.append(image)
    image_stu_id = list(dict.fromkeys(image_stu_id))
    c = json.dumps(dict(result_list=result_list, user=user_details, ques=objects_list, obj=obj, subj=subj,
                        obj_testname=obj_testname, subj_testname=subj_testname,
                        image=image_details, image_stu_id=image_stu_id), default=json_serial)
    # return jsonify({"result":result_list, "user":user_details})
    return c


@app.route('/evaluate', methods=['POST', 'GET'])
def evaluate():
    c = []
    n = request.form.get('rollno')
    g = request.form.get('index')
    h = request.form.get('user')
    k = request.form.get('ques_len')
    ll = request.form.get('test_id')
    m = request.form.get('result_id')
    # print(n, g, h, k, ll, m)
    start = int(g) - int(k)
    end = int(g)
    get_res = Result.query.filter_by(user_id=int(n), test_id=int(ll)).all()
    for i in range(start, end):
        m = request.form['marks_obt_' + str(i)]
        c.append(m)
    j = 0
    for res in get_res:
        res.total_marks = c[j]
        j += 1
        db.session.commit()
    return json.dumps(dict(status='ok', data=c))


@app.route('/evaluate_by_id', methods=['POST', 'GET'])
def evaluate_by_id():
    c = []
    n = request.form.get('rollno')
    g = request.form.get('index')
    h = request.form.get('user')
    k = request.form.get('ques_len')
    ll = request.form.get('test_id')
    # print(n, g, h, k, ll)
    start = int(g) - int(k)
    end = int(g)
    get_res = Result.query.filter_by(user_id=int(n), test_id=int(ll)).all()
    # print(get_res)
    for i in range(start, end):
        m = request.form['eval_marks_obt_' + str(i)]
        c.append(m)
    j = 0
    for res in get_res:
        res.total_marks = c[j]
        j += 1
        db.session.commit()
    return json.dumps(dict(status='ok', data=c))


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
    res = Result.query.filter_by(user_id=current_user.id).all()
    res_test_id = []
    for r in res:
        res_test_id.append(r.test_id)
    res_test_id = list(dict.fromkeys(res_test_id))
    for t in res_test_id:
        paper_get = Paperdetails.query.filter_by(test_id=t)
        ques = Questions.query.filter_by(test_id=t)
    # print(paper_get)
    # print(ques)
    return render_template('student/pre-exam.html')


@app.route('/camera', methods=['POST', 'GET'])
def camera():
    if request.method == 'POST':
        print(request.form.getlist('datauri'))
        datauri = request.form.getlist('datauri')
        # for d in datauri:
        #     print(base64.b64decode(d))
        test_id = request.form.get('test_id')
        for img_data in datauri:
            img = image_data(image=img_data, user_id=current_user.id, test_id=test_id)
            db.session.add(img)
            db.session.commit()
    return 'Ok'


@app.route('/delete_img', methods=['GET', 'POST'])
def delete_img():
    get_path = request.args.getlist('host[]')
    for i in get_path:
        os.remove(os.getcwd() + i)
    print("deleted")
    return json.dumps(dict(status='ok'))


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
            logout_user()
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
        flash('The Password has been Successfully Changed! Please Log In')
        return redirect(url_for('index'))
    return render_template('new_password.html')


@app.route('/edit_ques/<test_id>', methods=['POST', 'GET'])
def edit_ques(test_id):
    ques = Questions.query.filter_by(test_id=test_id).all()
    faculty_post = Paperdetails.query.filter_by(test_id=test_id).all()
    return render_template('faculty/edit_test.html', post=faculty_post, ques=ques)


@app.route('/updateques', methods=['GET', 'POST'])
def updateques():
    sem = []
    sec = []
    paper_test_id = request.form['test_id']
    test_detailss = Paperdetails.query.filter_by(test_id=paper_test_id).first()
    test_question = Questions.query.filter_by(test_id=paper_test_id).all()
    max_ques = 1
    if request.method == 'POST':
        if request.form.get("modal", "") == "1":
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
            duration = int(((int(hour) * 60) + int(minute)) * 60)
            for sem1 in semester:
                sem.append(sem1)
            for sec1 in section:
                sec.append(sec1)
            semester = str(sem)[1:-1].replace("'",
                                              "").replace(",", "")
            section = str(sec)[1:-1].replace("'",
                                             "").replace(",", "")
            if not section:
                section = str('A B C D')
            test_detailss.testname = name
            test_detailss.description = description
            test_detailss.college = college
            test_detailss.branch = branch
            test_detailss.semester = semester
            test_detailss.section = section
            test_detailss.subject = subject
            test_detailss.totalques = total_ques
            test_detailss.totaltime = duration
            test_detailss.testtype = test_type
            test_detailss.user_id = current_user.id
            test_detailss.scheduled_date = scheduled_date
            test_detailss.start_time = st_time
            test_detailss.end_time = en_time
            test_detailss.date_posted = datetime.now()
            if test_type == 'objective':
                correct_ans = request.form['correct_answer']
                wrong_ans = request.form['minus_mark']
                test_detailss.correct_ans = correct_ans
                test_detailss.wrong_ans = wrong_ans
            db.session.commit()
        elif request.form.get("obj", "") == "0":
            for q in test_question:
                q.question = request.form['ques_' + str(max_ques)]
                q.op1 = request.form['op1_' + str(max_ques)]
                q.op2 = request.form['op2_' + str(max_ques)]
                q.op3 = request.form['op3_' + str(max_ques)]
                q.op4 = request.form['op4_' + str(max_ques)]
                q.obj_ans = request.form['obj_ans_' + str(max_ques)]
                max_ques += 1
                db.session.commit()
            flash('Paper updated successfully', 'primary')
            return redirect(url_for('faculty_login'))
        else:
            for s in test_question:
                s.question = request.form['ques_' + str(max_ques)]
                s.marks_assign = request.form['marks_assign_' + str(max_ques)]
                max_ques += 1
                db.session.commit()
            flash('Paper updated successfully', 'primary')
            return redirect(url_for('faculty_login'))
        return redirect(url_for('edit_ques', test_id=paper_test_id))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
