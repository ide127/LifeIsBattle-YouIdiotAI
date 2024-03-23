from http import client
import time
from django.conf import settings
from openai import OpenAI
import requests 

class SingletonOpenAI:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            cls._instance = OpenAI(api_key=settings.OPENAI_API_KEY)
        return cls._instance

def get_ai_response(message, thread_id):
    def extract_barista_speech(text):
        start_tag = "[[barista's speech start]]"
        end_tag = "[[barista's speech end]]"
        
        start_index = text.find(start_tag) + len(start_tag)
        end_index = text.find(end_tag)
        
        if start_index == -1 or end_index == -1 or end_index <= start_index:
            return "No barista's speech found."
        
        barista_speech = text[start_index:end_index]
        return barista_speech
    def retrieve_message(thread_id, message_id):
        # Retrieve the message from the thread
        client = SingletonOpenAI.get_instance()
        messages = client.beta.threads.messages.list(
            thread_id=thread_id,
            order="asc",
            after=message_id
        )
        if messages.data[0].content[0].type == "text":
            message = messages.data[0].content[0].text.value
        elif messages.data[0].content[0].type == "image_file":
            message = None
        return {"type": messages.data[0].content[0].type, "value": extract_barista_speech(message)}
    def retrieve_run(thread_id, run_id):
        client = SingletonOpenAI.get_instance()
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run
    
    client = SingletonOpenAI.get_instance()
    
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="[[customer's speech start]]" + message + "[[customer's speech end]]"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=settings.OPENAI_ASSISTANT_ID,
    )
    # using runs.retrieve, check the status of the run every 3 seconds
    # if run.status == "complete", retrieve the answer message from the thread.
    # if run.status is not "queued" or "in_progress" or "requires_action", 
    # return an error message.
    run = retrieve_run(thread_id, run.id)
    if run.status == "completed":
        return retrieve_message
    else :
        while run.status in ["queued", "in_progress", "requires_action"]:
            time.sleep(1)
            run = retrieve_run(thread_id, run.id)
    
    if run.status == "completed":
        return retrieve_message(thread_id, message.id)
    else :
        return {"error": "An error occurred while retrieving AI response."}