from openai import OpenAI
import os

# client = OpenAI(
#             organization=os.environ['OPENAI_ORGANIZATION_ID'],
#             api_key=os.environ['OPENAI_API_KEY'],
#         )

def create_run(self,thread_id, assistant_id):
    run = self.client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        stream=True
    )

    return run

def retrieve_run(self,run_id, thread_id):
    run = self.client.beta.threads.runs.retrieve(
        run_id=run_id,
        thread_id=thread_id
    )

    return run



   