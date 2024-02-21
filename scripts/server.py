from flask import Flask, request, send_from_directory, redirect
import requests
import argparse
import os
import sys

# Determine the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up argument parsing
parser = argparse.ArgumentParser(description='A simple proxy server that also serves static files and proxies requests.')
parser.add_argument('--port', type=int, default=5000, help='Port to run the Flask server on (default: 5000)')
parser.add_argument('--static-folder', default='static', help='Folder from which to serve static files (default: "static")')
parser.add_argument('--external-api', required=True, help='The external API endpoint to proxy requests to')
args = parser.parse_args()

# Resolve the static folder path relative to the script's location
static_folder_path = os.path.join(BASE_DIR, args.static_folder)

# Verify the static directory exists
if not os.path.exists(static_folder_path):
    print(f"Error: The specified static folder '{static_folder_path}' does not exist.")
    sys.exit(1)

app = Flask(__name__)

@app.route('/proxy/<path:endpoint>', methods=['GET', 'POST'])
def proxy_request(endpoint):
    print(f'Proxying request to {args.external_api}{endpoint}\nrequest.args: {request.args}\nrequest.json: {request.json}')
    if request.method == 'GET':
        response = requests.get(args.external_api, params=request.args)
    elif request.method == 'POST':
        response = requests.post(args.external_api, json=request.json)
    return (response.content, response.status_code, response.headers.items())


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(static_folder_path, path)

@app.route('/')
def redirect_root():
    return redirect('/index.html')

if __name__ == '__main__':
    # Print the clickable URL
    print(f"Starting server. Visit http://localhost:{args.port}/")
    
    # Run the Flask application on the specified port and accessible from any address
    app.run(debug=True, port=args.port, host='0.0.0.0')
