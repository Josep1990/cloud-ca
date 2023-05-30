from flask import Flask
from flask import request
import jwt
from time import time
import os

app = Flask(__name__)

# TODO: We will come back to this
users = [
    {
        "username": "david",
        "password": "my-secret"
    },
    {
        "username": "test",
        "password": "my-secret-too"
    }
]

def generate_jwt_token(username):
    seconds_now = time()
    return jwt.encode(
        {   "username": username, 
            "iat": seconds_now,
            "exp": seconds_now + 30000
        },
        os.environ.get('JWT_SECRET'),
        algorithm="HS256"
    )

@app.route("/authorize")
def authorize():
    username = request.args.get('username')
    password = request.args.get('password')
    if username and password:
        for user in users:
            if username == user["username"] and password == user["password"]:
                return {"token": generate_jwt_token(user["username"])}
    return {"error": "user not found"}, 401

if __name__ == '__main__':
    if not os.environ.get('JWT_SECRET'):
        print("No JWT_SECRET variable found")
        exit(1)
    app.run(host='0.0.0.0')