from flask import Flask, request, redirect, url_for, jsonify
import logging
import requests
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from datetime import date, timedelta
from flask import session

app = Flask(__name__)

app.secret_key = 'some_random_secret_key'  # Change this to a proper secret key for your application

# Load client secrets from your .json file
with open('credentials_2.json', 'r') as f:
    client_config = json.load(f)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
REDIRECT_URI = 'https://localhost:8080/visitors'
flow = Flow.from_client_config(
    client_config=client_config,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route("/")
def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-RW8X8N6FVS"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-RW8X8N6FVS');
    </script>
    """
    message = "Hello World 🚀"
    button_google = '''
    <form action="/make_google_request" method="get">
        <input type="submit" value="Fetch Google Cookies">
    </form>
    '''
    button_visitors = '''
    <form action="/index" method="get">
        <input type="submit" value="Get Number of Visitors">
    </form>
    '''
    return prefix_google + message + "<br>" + button_google + button_visitors

logging.basicConfig(level=logging.DEBUG)

@app.route('/logger')
def logger():
    app.logger.info("Ceci est un log côté serveur (backend)!")
    return "<script>console.log('Ceci est un log côté client (frontend)!');</script>"

@app.route('/textbox', methods=['GET', 'POST'])
def textbox():
    message = ""
    if request.method == 'POST':
        message = request.form.get('message')
        app.logger.info(f"Message from textbox: {message}")

    return '''
        <form method="post">
            <input type="text" name="message">
            <input type="submit" value="Log Message">
        </form>
    '''

@app.route('/make_google_request')
def make_google_request():
    req = requests.get("https://www.google.com/")
    cookies = req.cookies._cookies
    cookies_str = "\n".join([f"{i} {j} {k} {cookies[i][j][k].value}" for i in cookies for j in cookies[i] for k in cookies[i][j]])
    return cookies_str

@app.route('/make_ganalytics_request')
def make_ganalytics_request():
    ganalytics_url = "https://analytics.google.com/analytics/web/#/report-home/a164062586w272485488p243020933"
    req = requests.get(ganalytics_url)
    status_code = req.status_code
    response_text = req.text
    return jsonify(status_code=status_code, text=response_text)

""""
@app.route('/root')
def root():
    return "Hello from Space! 🚀"
"""

@app.route('/index')
def index():
    authorization_url, state = flow.authorization_url(prompt='consent', include_granted_scopes='true')
    # Store state in session for further use
    session['state'] = state
    return redirect(authorization_url)


@app.route('/visitors')
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('get_ga_data'))


@app.route('/get_ga_data')
def get_ga_data():
    # Get the credentials from the session
    creds = session.get('credentials')
    credentials = Credentials(
        token=creds['token'],
        refresh_token=creds['refresh_token'],
        token_uri=creds['token_uri'],
        client_id=creds['client_id'],
        client_secret=creds['client_secret'],
        scopes=creds['scopes']
    )

    service = build('analytics', 'v3', credentials=credentials)
    today = date.today().strftime('%Y-%m-%d')
    start_date = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')

    property_id = 'properties/408224738'
    response = service.data().ga().get(
        ids='ga:' + property_id.split('/')[-1],  # The "ga:" prefix is typically required
        start_date=start_date,
        end_date=today,
        metrics='ga:activeUsers'
    ).execute()

    visitors_count = response.get('totals', [{}])[0].get('values', [0])[0]

    return f"Number of visitors for the last 30 days: {visitors_count}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))