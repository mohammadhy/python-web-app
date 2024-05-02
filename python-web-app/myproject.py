import logging
from flask import Flask
from flask_cors import CORS
from redis import Redis, ConnectionError
from elasticapm.contrib.flask import ElasticAPM
from prometheus_flask_exporter import PrometheusMetrics
app = Flask(__name__)
CORS(app)
apm = ElasticAPM(app, logging=True)
redis = Redis(host="redis.redis-db", port=6379, password="123")
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
    app.logger.info("Log From main function")
    return "<h1 style='color:blue'>main!</h1>"
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

