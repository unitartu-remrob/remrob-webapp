from flask import Flask, request
from git_clone import clone
from git_commit_push import commit_push
import requests, json, os

app = Flask(__name__)

database = {'2b9ca7a1f2484df88d':'test', '32b9ca7a1f2484df88':'test2'} # database simulation

repos_root = '/home/am/repos'
cloning_root = 'https://gitlab.ut.ee/aleksandr.makarov/'
token_name = 't1'
token = 'V6FgRAo8JkMiBhgT98Yc'


# TODO: implement this thingie with database
def match_session_to_username(session_token: str) -> str:
    """Matches session id sent as a request from a container with the right user name

    Args:
        session_token (str): session token from the container

    Returns:
        str: user name or 'error'
    """
    if database.get(session_token, 0):
            return database[session_token]
    else:
        return 'error'

def check_project(project_name:str):
    """Checks if repo exists, if not then creating it

    Args:
        project_name (str): user name

    Returns:
        str: status
    """
    url = "https://gitlab.ut.ee/api/v4/projects"
    project_path = project_name
    description = f"Project of the user: {project_name}"

    payload = json.dumps({
    "name": project_name,
    "description": description,
    "path": project_path,
    "initialize_with_readme": "true"
    })
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if isinstance(response.json(), dict):
        resp = 'User exists' if response.json().get('message', 0) else 'User repo was created'
    else:
        resp = 'User exists'

    return resp


@app.route("/")
def hello_world():
    return "<p>This is just an example!</p>"

@app.route('/api/v1/reclone', methods=['GET'])
def api_repo_reclone():
    """This function takes token as the request argument parses to get username after which it removes the repo and clones it again 

    Returns:
        _type_: _description_
    """

    if 'token' in request.args:
        session_token = request.args['token']
    else:
        return 'error: no session token frovided'

    user_name = match_session_to_username(session_token)

    if user_name == 'error': return 'error: user not found'

    force = False
    if 'force' in request.args:
        if 'true' == request.args['force'].lower():
            force = True  

    return clone(cloning_root+user_name, token_name, token, repos_root, force)


@app.route('/api/v1/clone', methods=['GET'])
def api_repo_clone():
    print(request.args)

    if 'user_name' in request.args:
        user_name = request.args['user_name']
    else:
        return 'error: no user specified'

    force = False
    if 'force' in request.args:
        if 'true' == request.args['force'].lower():
            force = True        

    return clone(cloning_root+user_name, token_name, token, repos_root, force)

@app.route('/api/v1/check_user', methods=['GET'])
def api_check_user():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
    else:
        return 'error: no user specified'
    return check_project(user_name)


@app.route('/api/v1/commit_push', methods=['GET'])
def api_repo_commit_push():

    if 'token' in request.args:
        session_token = request.args['token']
    else:
        return 'error: no session token provided'

    user_name = match_session_to_username(session_token)

    if user_name == 'error': return 'error: user not found'

    path = os.path.join(repos_root, user_name)

    print(path)

    return commit_push(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4050)