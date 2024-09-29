from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS
from redis import Redis, ConnectionError
from elasticapm.contrib.flask import ElasticAPM
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
apm = ElasticAPM(app, logging=True)
redis = Redis(host="redis.db", port=6379, password="123")

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

app.config['ELASTIC_APM'] = {
'SERVICE_NAME': 'python-flaskk-app',
'SERVER_URL': 'http://localhost:8200',
'ENVIRONMENT': 'production',
}
@app.route("/")
def main():
    return "<h1 style='color:red'>Home Lab Hy</h1>"
@app.route("/second")
def second():
    return "<h1 style='color:red'>second Page </h1>"
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


def all_required_services_are_running():
    try:
        redis.ping()
        return True
    except ConnectionError:
        return False
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

