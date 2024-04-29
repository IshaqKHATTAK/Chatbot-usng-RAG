from flask import Flask, request, jsonify
from assistant import create_client, create_thread, chat_with_assist
import os
from flask_cors import CORS, cross_origin
client = None
thread_id = None

app = Flask(__name__)
CORS(app) 

assis_id = os.getenv("ASSISTANT_ID") # you can access the OPENAI_API_KEY from .env
openai_api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def hello_world():
    return "<p>Hello, !</p>"

@app.route('/ask', methods=['POST'])
def question_answer():
    # Extract the message from the request body
    data = request.json
    message = data.get('message')
    global client
    global thread_id
   
    # Run once to create the client and thread
    if client is None:
        client = create_client(openai_api_key)
        thread = create_thread(client)
        thread_id = thread.id
    
    if message:
        # Pass the message to the chat_with_assist function
        response = chat_with_assist(message, thread_id, assis_id)
        print('response of ',response)
        return jsonify({'message': response})
    else:
        return jsonify({'error': 'No message provided'}), 400
    

if __name__ == '__main__':
    app.run(debug=True)