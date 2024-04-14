import json
from fastapi import FastAPI, Response,status
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
import os
import mux_python
import subprocess


app = FastAPI()

load_dotenv()
# @app.websocket("/")
# async def websocket_ping(websocket:WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()

# @app.get("/")
# async def sample():
#     serializer = {
#         "status_code":status.HTTP_200_OK,
#         "message":"Sample",
#         "data":None
#     }
#     return Response(
#         content = jsonable_encoder(json.dumps(serializer)),
#         media_type="application/json",
#         status_code=serializer['status_code'],
#     )

@app.get("/")
async def get_stream_key():
    configuration = mux_python.Configuration()
    configuration.username = os.getenv('MUX_TOKEN_ID')
    configuration.password = os.getenv('MUX_TOKEN_SECRET')

    #Store into redis

    live_api = mux_python.LiveStreamsApi(mux_python.ApiClient(configuration))
    new_asset_settings = mux_python.CreateAssetRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC])
    create_live_stream_request = mux_python.CreateLiveStreamRequest(playback_policy=[mux_python.PlaybackPolicy.PUBLIC], new_asset_settings=new_asset_settings)
    create_live_stream_response = live_api.create_live_stream(create_live_stream_request)
    
    serializer = {
        "status_code":status.HTTP_200_OK,
        "message":"Sample",
        # "data":jsonable_encoder(json.dumps(create_live_stream_response.__dict__))
        "data":{
            "stream_key":create_live_stream_response.data.stream_key,
            "status":create_live_stream_response.data.status,
            "reconnect_window":create_live_stream_response.data.reconnect_window,
            "playback_ids":[
                {
                    "id":create_live_stream_response.data.playback_ids[0].id,
                    "policy":create_live_stream_response.data.playback_ids[0].policy,
                }
            ],
            "id":create_live_stream_response.data.id,
            "created_at":create_live_stream_response.data.created_at,
            "latency_mode":create_live_stream_response.data.latency_mode,
            "max_continuous_duration":create_live_stream_response.data.max_continuous_duration,
        },
        # "data":jsonable_encoder(json.dumps(create_live_stream_response.data.__dict__))
    }
    return Response(
        content = jsonable_encoder(json.dumps(serializer)),
        media_type="application/json",
        status_code=serializer['status_code'],
    )

@app.get("/get")
async def get_live_streams():
    # Define the command to execute using curl
    MUX_TOKEN_ID = os.getenv['MUX_TOKEN_ID']
    MUX_TOKEN_SECRET = os.getenv['MUX_TOKEN_SECRET']
    url = f'''
    curl https://api.mux.com/video/v1/live-streams \
    -X GET \
    -H "Content-Type: application/json" \
    -u ${MUX_TOKEN_ID}:${MUX_TOKEN_SECRET}
    '''
    command = ['curl', '-s', '-o', '-', url]

    # Execute the curl command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)
    serializer = {
        "status_code":status.HTTP_200_OK,
        "message":"Sample",
        "data":json.dumps(result)
    }
    return Response(
        content = jsonable_encoder(json.dumps(serializer)),
        media_type="application/json",
        status_code=serializer['status_code'],
    )