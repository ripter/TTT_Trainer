from flask import Flask, request, send_from_directory, redirect, jsonify
import requests
import argparse
import os
import sys

from mlx_lm import load, generate

# Determine the absolute path to the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up argument parsing
parser = argparse.ArgumentParser(description='A simple proxy server that also serves static files and proxies requests.')
parser.add_argument('--port', type=int, default=4400, help='Port to run the Flask server on (default: 4400)')
parser.add_argument('--static-folder', default='static', help='Folder from which to serve static files (default: "static") This must be a subdirectory of the current directory.')
parser.add_argument('--model', type=str, help='Path to local model or or the huggingface repository.')
parser.add_argument('--lora', type=str, help='Path to the LoRA adapter file.')
args = parser.parse_args()

# Resolve the static folder path relative to the script's location
static_folder_path = os.path.join(BASE_DIR, args.static_folder)

# Verify the static directory exists
if not os.path.exists(static_folder_path):
    print(f"Error: The specified static folder '{static_folder_path}' does not exist.")
    sys.exit(1)

# Verify the model folder exist
if not args.model or not os.path.exists(args.model):
    print(f"Error: Please specify a model.")
    sys.exit(1)

# If the LoRA adapter file is specified, verify it exists
if args.lora and not os.path.exists(args.lora):
    print(f"Error: The specified LoRA adapter file '{args.lora}' does not exist.")
    sys.exit(1)

# Attempt to load the model
if not args.lora:
    model, tokenizer = load(args.model)
else:
    model, tokenizer = load(args.model, adapter_file=args.lora)




# Create the Flask application
app = Flask(__name__)


# @app.route('/api/health', methods=['GET'])
# def get_health():
#     response = requests.get(f'{args.external_api}/health')
#     return (response.content, response.status_code, response.headers.items())

@app.route('/api/completion', methods=['POST'])
def post_completion():
    data = request.get_json()
    prompt = data.get('prompt', None)
    max_tokens = data.get('n_keep', 35)
    temp = data.get('temp', 0.8)

    # Give the AI the entire game log as the prompt.
    ai_response = generate(model, tokenizer, prompt, temp, max_tokens)
    return jsonify({
        "content": ai_response
    })
    # response = requests.post(f'{args.external_api}/completion', json=request.json)
    # return (response.content, response.status_code, response.headers.items())


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
