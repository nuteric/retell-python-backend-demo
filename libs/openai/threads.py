from openai import OpenAI
import os


# client = OpenAI(
#             organization=os.environ['OPENAI_ORGANIZATION_ID'],
#             api_key=os.environ['OPENAI_API_KEY'],
#         )

def create_thread(self):
    thread = self.client.beta.threads.create()
    return thread


def  get_last_message(self,thread_id):
    messages = self.client.beta.threads.messages.list(
        thread_id=thread_id
    )

    last_message_id = messages.last_id

    last_message = self.client.beta.threads.messages.retrieve(
        message_id=last_message_id,
        thread_id=thread_id,
    )

    return last_message