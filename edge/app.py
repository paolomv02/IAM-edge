import os

# Set environment variables
os.environ['BACKEND_URL'] = 'http://localhost:8080'
os.environ['JWT_TOKEN'] = 'eyJhbGciOiJIUzM4NCJ9.eyJzdWIiOiJkcml2ZXIiLCJpYXQiOjE3NTE3ODM4MTAsImV4cCI6MTc1MjM4ODYxMH0.H10Smoyt66-FIV2cQ_xFkjvqwXbmS8L-73OQ9ar4UJa8ZcInS6jL0hsX-itC6TUM'

from flask import Flask

from tracking.interfaces.services import tracking_api
from iam.interfaces.services import iam_api
from shared.infrastructure.database import init_db



app = Flask(__name__)
app.register_blueprint(tracking_api)
app.register_blueprint(iam_api)

first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")