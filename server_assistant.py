import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.websockets import WebSocketState
import asyncio

from llm_assistant import LlmAssistant
load_dotenv(override=True)

app = FastAPI()


@app.websocket("/llm-websocket/{call_id}")
async def websocket_handler(websocket: WebSocket, call_id: str):
    await websocket.accept()

    llm_client = LlmAssistant()

    # start of call
    response_id = 0

    # create a greeting message
    greeting_message = llm_client.draft_begin_messsage()

    # send greeting to websocket
    await websocket.send_text(json.dumps(greeting_message))

    async def stream_response(request):
        nonlocal response_id

        for event in llm_client.draft_response(request):
            await websocket.send_text(json.dumps(event))
            if request['response_id'] < response_id:
                return # new response needed, abondon this one

        
    try:
        while True:

            # receive events from websocket
            message = await websocket.receive_text()
            request = json.loads(message)

            # if event is update_only
            if request['interaction_type'] == 'update_only':
                # do nothing
                continue

            # if event is reminder_required
            if request['interaction_type'] == 'reminder_required':
                
                # send reminder to websocket
                reminder_message = llm_client.get_reminder_message()
                await websocket.send_text(json.dumps(reminder_message))
                continue

            # if event is response_required
            if request['interaction_type'] == 'response_required':

                # get response_id from event  
                response_id = request['response_id']  
                asyncio.create_task(stream_response(request))        

    except WebSocketDisconnect:
        print(f"LLM WebSocket disconnected for {call_id}")
    except Exception as e:
        print(f'LLM WebSocket error for {call_id}: {e}')
    finally:
        print(f"LLM WebSocket connection closed for {call_id}")

                

