import os
from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
CORS(app)

from backend import authentication, read_token  # nopep8


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return f"""
    <h1>Oh, hello there!</h1>
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcReRPKmuBvP_y4usgsoAYZYe1esuXKGM1ilWA&usqp=CAU" />
    <p>Unfortunately there's nothing to see here.</br>Please use a proper url.
    </br></br></br>Thanks for understanding.</p>
    """


@app.route('/auth', methods=['POST'])
def auth():
    result = authentication(request.json)
    if result:
        response = app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps({
                "success": 0,
                "resp": "Record not found"}),
            status=200,
            mimetype='application/json'
        )

    return response


@app.route('/read', methods=['POST'])
def read():
    result = read_token(request.json)
    if result:
        response = app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps("Record no found"),
            status=200,
            mimetype='application/json'
        )

    return response


if __name__ == "__main__":
    app.run()
