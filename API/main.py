import asyncio
import sched,time
from fastapi import FastAPI, WebSocket
import uvicorn
import poseEstimation
import json
import threading
import mediapipe as mp

app = FastAPI(title='ESMA API')
mpPose = mp.solutions.pose


class connectionUser:
    def __init__(self, id, pose):
        self.id = id
        self.currFrame = None
        self.pose = pose
    id: str
    pose:any
    currFrame: str

connections = []

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(updateFrames())

async def updateFrames():
    while True:
        await poseEstimation.receivedFrameData(connections)
        await asyncio.sleep(0.1)

async def updateConnection (clientData):
    user = next(x for x in connections if x.id == clientData["id"])
    if(user):
        user.currFrame = clientData["frame"];


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            if(data["type"] == "init"):
                connections.append(connectionUser(data["id"], mpPose.Pose()))
            else:
                await updateConnection(data)

        except Exception as e:
            print("error: ", e)
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
