from flask import Flask, request, send_from_directory, redirect, Response, jsonify
import requests
import argparse
import os
import sys

# Determine the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up argument parsing
parser = argparse.ArgumentParser(description='A simple proxy server that also serves static files and proxies requests.')
parser.add_argument('--port', type=int, default=4400, help='Port to run the Flask server on (default: 5000)')
parser.add_argument('--static-folder', default='static', help='Folder from which to serve static files (default: "static")')
parser.add_argument('--external-api', default='http://localhost:8080', help='The external API endpoint to proxy requests to')
args = parser.parse_args()

# Resolve the static folder path relative to the script's location
static_folder_path = os.path.join(BASE_DIR, args.static_folder)

# Verify the static directory exists
if not os.path.exists(static_folder_path):
    print(f"Error: The specified static folder '{static_folder_path}' does not exist.")
    sys.exit(1)

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def get_health():
    response = requests.get(f'{args.external_api}/health')
    return (response.content, response.status_code, response.headers.items())


@app.route('/api/completion', methods=['POST'])
def post_completion():
    response = requests.post(f'{args.external_api}/completion', json=request.json)
    return (response.content, response.status_code, response.headers.items())

# @app.route('/proxy/<path:endpoint>', methods=['GET', 'POST'])
# def proxy_request(endpoint):
#     print(f'Proxying request to {args.external_api}{endpoint}\nrequest.args: {request.args}\nrequest.json: {request.json}')
#     if request.method == 'GET':
#         response = requests.get(args.external_api, params=request.args)
#     elif request.method == 'POST':
#         response = requests.post(args.external_api, json=request.json)
#     return (response.content, response.status_code, response.headers.items())

# @app.route('/proxy/<path:endpoint>', methods=['GET', 'POST'])
# def proxy_request(endpoint):
#     # Construct the full URL by appending the endpoint to the base external API URL
#     url = f"{args.external_api}/{endpoint}"
#     print(f'Proxying request to {url}\nrequest.args: {request.args}\nrequest.json: {request.json}')
    
#     headers = {}
#     # Pass along the headers from the original request, if present
#     headers.update(request.headers)

#     # Include more headers as needed, especially if the API requires specific headers to be set.
#     # For example, forwarding the Content-Type header for POST requests:
#     # if 'Content-Type' in request.headers:
#     #     headers['Content-Type'] = request.headers['Content-Type']
    
#     try:
#         if request.method == 'GET':
#             response = requests.get(url, params=request.args, headers=headers)
#         elif request.method == 'POST':
#             # Ensure the JSON body is forwarded correctly.
#             response = requests.post(url, json=request.json, headers=headers)
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return Response("Failed to proxy request", status=502)  # Bad Gateway to indicate upstream failure

#     # Forward the response content, status code, and headers back to the client
#     return Response(response.content, status=response.status_code, headers=dict(response.headers))

# @app.route('/proxy/<path:endpoint>', methods=['GET', 'POST'])
# def proxy_request(endpoint):
#     url = f"{args.external_api}/{endpoint}"
#     print(f'Proxying request to {url}\nrequest.args: {request.args}\nrequest.json: {request.json}')
#     return f'Proxying request to {url}\nrequest.args: {request.args}\nrequest.json: {request.json}', 200

#     # Prepare headers for the proxied request
#     headers_to_forward = {'Accept': request.headers.get('Accept')}
#     headers_to_forward['Content-Type'] = request.headers.get('Content-Type')
#     # if request.method == 'POST' and 'Content-Type' in request.headers:
#     #     headers_to_forward['Content-Type'] = request.headers.get('Content-Type')

#     try:
#         if request.method == 'GET':
#             response = requests.get(url, params=request.args, headers=headers_to_forward)
#         elif request.method == 'POST':
#             # Assuming you want to forward a JSON body if present
#             data = request.json if request.is_json else {}
#             response = requests.post(url, json=data, headers=headers_to_forward)
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return Response("Failed to proxy request", status=502)  # Use 502 Bad Gateway to indicate an upstream error

#     # Forward the proxied response back to the client
#     return Response(response.content, status=response.status_code, headers=dict(response.headers))




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
