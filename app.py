from flask import Flask, render_template, redirect, request, url_for, session, flash
from werkzeug.utils import secure_filename
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
import re
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail,Message

app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = b"\x07\x92\xde\xa5%YP\xf6\xd2\xb4\xad\x13," \
                           b"\x7f\x949\x89?'A\xb0\x9ep\x0f\x8b=\xfe\xef\x93\xf7:i\xe6\xba<_Y(" \
                           b"\xebe\xf6o\x90'\xc3?\x9f\x0c\x93\xad[" \
                           b"\xf3\xb9\xc4\x95\xce\xc18\x87*m\xd3\x805\xcf\xf7\xf0\xcf\x91\xf9]\xc7\xc5$<\xe0O\x8cx\x84\x99\xd8" \
                           b"\x8eqF*G\xa6i[H\xb3Yp\xa0\xa6QB\xeebt\xc7\xd7\xb1\xbe{" \
                           b"D\xb1%\xa6e!\xd56\xd7\x8aZ2\x8aPD\xa1\xf3\x12\\\x16\xa2\x85 "

app.config["MYSQL_HOST"] = os.environ.get('MYSQL_HOST')
app.config["MYSQL_USER"] = os.environ.get('MYSQL_USER')
app.config["MYSQL_PASSWORD"] = os.environ.get('MYSQL_PASSWORD')
app.config["MYSQL_DB"] = os.environ.get('MYSQL_DB')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('Email_ADD')
app.config['MAIL_PASSWORD'] = 'equiqhpzpegsdnzl'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)


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
    for id in user_id:
        if id == '3035' or id == '3014' or id == '3036':
            return 1
        else:
            return 0


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def index():
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


@app.route('/student/main')
def student_login():
    return "Hii Buddy"


@app.route('/faculty/main')
def faculty_login():
    return "Hii Sir"


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/student')
def student():
    return render_template('student_register.html')


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
        user = Users.query.filter_by(email = request.form['Remail']).first()
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
