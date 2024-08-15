import logging
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo
from flask_bcrypt import Bcrypt
from redis import Redis, ConnectionError
from elasticapm.contrib.flask import ElasticAPM
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'
apm = ElasticAPM(app, logging=True)
redis = Redis(host="redis.db", port=6379, password="123")

app.config['MYSQL_HOST'] = 'mysql-service.db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    submit = SubmitField('Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        user = cur.fetchone()
        cur.close()
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = user['username']
            return redirect(url_for('main'))
        else:
            return 'Invalid credentials'
    return render_template('login.html', form=form)



metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

logging.basicConfig(filename='record.log',format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s' , level=logging.DEBUG)


app.config['ELASTIC_APM'] = {
'SERVICE_NAME': 'python-flaskk-app',
'SERVER_URL': 'http://localhost:8200',
'ENVIRONMENT': 'production',
}
@app.route("/")
def main():
    if 'username' in session:
        app.logger.info("Log From main function")
        return f"<h1 style='color:blue'>Welcome {session['username']}!</h1>"
    else:
        return redirect(url_for('login'))
@app.route("/second")
def second():
    app.logger.error("Log From second function")
    return "<h1 style='color:red'>second</h1>"
@app.route("/redis")
def write():
    redis.set("KeyName", "ValueName")
    return "<h1 style='color:green> Write Success</h1>"
@app.route('/health')
def health_check():
    if all_required_services_are_running():
        return 'OK', 200
    else:
        return 'Service Unavailable', 500

app.route('/metrics')
def metrics():
    return { 
            'status' '200'
            }

def all_required_services_are_running():
    try:
        redis.ping()
        return True
    except ConnectionError:
        return False
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

