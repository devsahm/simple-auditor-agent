from openai import OpenAI
import os
from dotevn import load_dotenv
from actions import get_response_time
from prompts import system_prompt
from json_helper import extract_json


# Load Environemental variable
load_dotenv()

#instantiate OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_text_with_conversation(messages, model="gtp-3.5-turbo"):
    response = openai_client.chat.conversations.create(
        model = model,
        messages = messages
    )
    return response.choices[0].message.content


# Available Actions Are
available_actions = {
    "get_response_time" : get_response_time
}

#user prompt
user_prompt = "what is the response time of google.com?"


messages = [
    {"role":"system", "content": system_prompt},
    {"role":"user", "content": user_prompt}
]

turns_count = 0
max_turns = 5

while turns_count < max_turns :
    print(f"Loop: {turns_count}")
    print('-------------------------------------')
    turns_count +=1 

    response = generate_text_with_conversation(messages, model="gtp-4")

    print(response)

    json_function = extract_json(response)
    
    if json_function:
        function_name = json_function[0]['function_name']
        function_params = json_function[0]['function_params']

        if function_name not in available_actions:
            raise Exception(f"Unnown action: {function_name}: {function_params}")
        
        print(f"runing ------ {function_name}:{function_params}")

        #get the action function and call it
        action_function = available_actions[function_name]
        result = action_function(**function_params)

        function_result_messages = f"Action_Response: {result}"
        #append the result to the message
        messages.append({"role": "user", "content": function_result_messages})

        print(function_result_messages)
    else:
        break


















