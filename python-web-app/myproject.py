from flask import Flask
from flask_cors import CORS
from redis import Redis
from elasticapm.contrib.flask import ElasticAPM
app = Flask(__name__)
CORS(app)
apm = ElasticAPM(app)
redis = Redis(host="redis.redis-db.svc.cluster.local", port=6379, password="123")

app.config['ELASTIC_APM'] = {
'SERVICE_NAME': 'python-flaskk-app',
'SERVER_URL': 'http://localhost:8200',
'ENVIRONMENT': 'production',
}
@app.route("/")
def main():
    return "<h1 style='color:blue'>main!</h1>"
@app.route("/second")
def second():
    return "<h1 style='color:red'>second</h1>"
@app.route("/redis")
def write():
    redis.set("KeyName", "ValueName")
    return "<h1 style='color:green> Write Success</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

