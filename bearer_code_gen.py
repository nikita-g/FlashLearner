CLIENT_ID = "wBnJTc87dG"
CLIENT_SECRET = "hMt6q7UvR3Gq3stPxbcAJe"
REDIRECT_URI = "http://localhost:65010/quizlet_callback"

from flask import Flask
app = Flask(__name__)

### APPLICATION USED TO GET BEARER TOKEN
### 1.) RUN APPLICATION
### 2.) OPEN http://127.0.0.1:65010/
### 3.) USE THE BUTTONS TO GET BEARER CODE
@app.route('/')
def homepage():
	text = '<a href="%s">Authenticate with quizlet</a>'
	return text % make_authorization_url()

def make_authorization_url():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
	params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "temporary",
			  "scope": "identity"}
	import urllib
	url = "https://quizlet.com/authorize?response_type=code&client_id=wBnJTc87dG&scope=read&state=RANDOM_STRING&redirect_uri=http://localhost:65010/quizlet_callback"
	return url

from flask import abort, request
@app.route('/quizlet_callback')
def reddit_callback():
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = request.args.get('state', '')
	if not is_valid_state(state):
		# Uh-oh, this request wasn't started by us!
		abort(403)
	code = request.args.get('code')
	# We'll change this next line in just a moment
	return "got a code! %s" % get_token(code)


import requests
import requests.auth
def get_token(code):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	response = requests.post("https://api.quizlet.com/oauth/token",
							 auth=client_auth,
							 data=post_data)
	token_json = response.json()
	return token_json["access_token"]


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True





if __name__ == '__main__':
	app.run(debug=True, port=65010)


