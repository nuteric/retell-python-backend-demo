from openai import OpenAI
import os

# client = OpenAI(
#             organization=os.environ['OPENAI_ORGANIZATION_ID'],
#             api_key=os.environ['OPENAI_API_KEY'],
#         )

def create_message(self, thread_id, role, content):
    message = self.client.beta.threads.messages.create(
        content=content,
        role=role,
        thread_id=thread_id
    )

    return message



