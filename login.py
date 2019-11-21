import requests
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/login")
def get_token():
    username = request.args.get('username')
    password = request.args.get('password')

    url = 'https://os.ncuos.com/api/user/token'

    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": username,
        "password": password
    }
    r = requests.post(url, headers=headers, json=body)
    return r.json()


if __name__ == '__main__':
    app.run(debug=True)
