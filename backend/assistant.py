import openai
import time
import logging
from datetime import datetime
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()
client = None
filename = f'order.json'

def take_order(timestamp, itmes, quantity):
    order_entry = {
        'timestamp': timestamp,
        'items': itmes,
        'quantity': quantity
        }

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    order_number = len(data) + 1
    data[str(order_number)] = order_entry
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=10)
        function_output = r"Your order has placed succesfully."
    except Exception as e:
        function_output = r"Your order has failed to save."

    return function_output

def create_client(openai_key):
   global client
   openai.api_key = openai_key
   client = openai.OpenAI()
   return client

def create_thread(client):
   thread = client.beta.threads.create()
   return thread

#this is for api
def chat_with_assist(user_input,thread_id,assis_id):
  message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assis_id)
  if run.required_action is None:
      pass
  else:
      for tool in run.required_action.submit_tool_outputs.tool_calls:
        function_arguments = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
        function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
        function_response = globals()[function_name](function_arguments["time_stamp"], function_arguments["itmes"], function_arguments["quantity"])
        

        run = client.beta.threads.runs.submit_tool_outputs(
          thread_id=thread_id,
          run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": tool.id,
                "output": function_response,
            }
        ],
      )

  while  run.status != 'completed':
    run = client.beta.threads.runs.retrieve(
    thread_id=thread_id,
    run_id=run.id)
    time.sleep(2)
  messages = client.beta.threads.messages.list(
  thread_id=thread_id)
  return messages.data[0].content[0].text.value



def chat_with_assistant(thread_id,assis_id):
  while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
      break

    message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input,
        )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assis_id)

    if run.required_action is None:
      pass
    else:
      for tool in run.required_action.submit_tool_outputs.tool_calls:
        function_arguments = json.loads(run.required_action.submit_tool_outputs.tool_calls[0].function.arguments)
        function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
        function_response = globals()[function_name](function_arguments["time_stamp"], function_arguments["itmes"], function_arguments["quantity"])
        

        run = client.beta.threads.runs.submit_tool_outputs(
          thread_id=thread_id,
          run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": tool.id,
                "output": function_response,
            }
        ],
      )

    while  run.status != 'completed':
      run = client.beta.threads.runs.retrieve(
      thread_id=thread_id,
      run_id=run.id)
      time.sleep(2)
    messages = client.beta.threads.messages.list(
    thread_id=thread_id)
    print(messages.data[0].content[0].text.value)


def main():
    global client
    # Run once to create the client and thread
    if client is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client = create_client(openai_api_key)
        thread = create_thread(client)
        assis_id = 'asst_3xxxxxxxxxxxxxx' # you can access the OPENAI_API_KEY from .env
    
    chat_with_assistant(thread.id, assis_id)

if __name__ == "__main__":
    main()