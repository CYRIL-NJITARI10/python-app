from flask import Flask, request, url_for, jsonify
import logging
import requests
import json
from datetime import date, timedelta
from flask import session

app = Flask(__name__)

# CSS pour styliser la page
# CSS pour styliser la page
css_style = '''
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }
        .container {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 0px 10px 0px #000;
            max-width: 600px;
        }
        h1 {
            color: #333;
        }
        .button-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .button {
            background-color: #007bff;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            text-transform: uppercase;
            cursor: pointer;
        }
        .button:hover {
            background-color: #0056b3;
        }
    </style>
'''

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
    message = "<h1>Hello World 🚀</h1>"
    button_textbox = '''
    <form action="/textbox" method="get">
        <input type="submit" class="button" value="Textbox">
    </form>
    '''
    button_google = '''
    <form action="/make_google_request" method="get">
        <input type="submit" class="button" value="Fetch Google Cookies">
    </form>
    '''
    button_google_analytics = '''
    <form action="/make_ganalytics_request" method="get">
        <input type="submit" class="button" value="Fetch Google Analytics Cookies">
    </form>
    '''
    button_visitors = '''
    <form action="/get_number_of_visitors" method="get">
        <input type="submit" class="button" value="Get Number of Visitors">
    </form>
    '''
    return prefix_google + css_style + '<div class="container">' + message + button_textbox + button_google + button_google_analytics + button_visitors + '</div>'


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

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
)
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'CyrildataSr-cf726b873030.json'

def get_number_of_visitors(property_id):
    client = BetaAnalyticsDataClient()
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="date")],
        metrics=[Metric(name="activeUsers")],
        date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    )

    response = client.run_report(request)

    # Parse the response to get the number of visitors
    number_of_visitors = None
    for row in response.rows:
        number_of_visitors = row.metric_values[0].value
        break  # Assuming you only need the first row

    return number_of_visitors

@app.route('/get_number_of_visitors')
def get_number_of_visitors_route():
    # Replace 'YOUR-GA4-PROPERTY-ID' with your Google Analytics 4 property ID
    property_id = "408224738"  # Replace with your property ID
    visitors = get_number_of_visitors(property_id)
    return f"Number of visitors: {visitors}"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context=('cert.pem', 'key.pem'))