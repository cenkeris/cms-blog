import requests
from flask import Flask, session, request

from services.contents import get_token

app = Flask(__name__)
app.secret_key = "MrqDYHY4oRYGko0p7QcoNVt4UqlujZAY"


from handlers.contents import init_handler

init_handler(app)


@app.before_request
def check_token():
    if request.path not in ['/logout']:
        if session.get('token'):

            url = "http://dev-management.dogannet.tv/api/me"
            headers = {
                'Authorization': 'Bearer {}'.format(session['token'])
            }

            response = requests.get(url, headers=headers)

            if response.status_code != 201:
                session['token'] = get_token(session['credentials'])


if __name__ == '__main__':
    app.run(debug=True)
