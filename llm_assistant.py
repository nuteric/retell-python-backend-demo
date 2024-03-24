from openai import OpenAI
import os
from libs.openai.threads import create_thread, get_last_message
from libs.openai.message import create_message
from libs.openai.run import create_run, retrieve_run

beginSentence = "Hello, I am Denise your AI dental assistant. How can I help you today?"

class LlmAssistant:
    def __init__(self):
        self.client = OpenAI(
            organization=os.environ['OPENAI_ORGANIZATION_ID'],
            api_key=os.environ['OPENAI_API_KEY'],
        )

        # create OpenAI thread
        self.thread = create_thread(self)

    def draft_begin_messsage(self):

        return {
            "response_id": 0,
            "content": beginSentence,
            "content_complete": True,
            "end_call": False,
        }

    def get_reminder_message(self):
        return {
            "response_id": 0,
            "content": "Please respond to the last message",
            "content_complete": True,
            "end_call": False,
        }
    
    def draft_response(self, request):

        # get transcript from event
        transcript = request['transcript']

        # get the last message from transcript
        last_message_in_transcript = transcript[-1]

        # if last message is from agent, skip
        if last_message_in_transcript['role'] == 'agent':
            return

        # if last message is from user
        if last_message_in_transcript['role'] == 'user':

            
            # add message to OpenAI thread
            message = create_message(self,
                thread_id=self.thread.id,
                role="user",
                content=last_message_in_transcript['content']
            )

            # create OpenAI run
            run = create_run(
                self,
                thread_id=self.thread.id,
                assistant_id=os.environ['OPENAI_ASSISTANT_ID']
            )

            # for each chunk in stream
            for chunk in run:

                # if chunk requires to call a tool (function call)\
                if chunk.event == "thread.run.requires_action":
                    # call the tool
                    continue
                
                if chunk.event == "thread.message.delta":
                    
                    # convert chunk to websocket response event object
                    response_event = {
                        "response_id": request['response_id'],
                        "content": chunk.data.delta.content[0].text.value,
                        "content_complete": False,
                        "end_call": False,
                    }

                    # send response object to websocket
                    yield response_event

                if chunk.event == "thread.run.complete":
                    # convert chunk to websocket response event object
                    response_event = {
                        "response_id": request['response_id'],
                        "content": chunk.data.delta.content[0].text.value,
                        "content_complete": True,
                        "end_call": False,
                    }

                    # send response object to websocket
                    yield response_event




        # return {
        #     "response_id": request['response_id'],
        #     "content": "testing response message for response id" + str(request['response_id']),
        #     "content_complete": True,
        #     "end_call": False,
        # }