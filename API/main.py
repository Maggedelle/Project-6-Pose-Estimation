from collections import defaultdict
from getpass import getuser
from fastapi import FastAPI, WebSocket
from pyparsing import And
import uvicorn
import poseEstimation
import mediapipe as mp
import calculator as calc
import time, threading, queue
import datetime as dt
import json
app = FastAPI(title='ESMA API')


mpPose = mp.solutions.pose


class connectionUser:
    def __init__(self, id, pose):
        self.id = id
        self.currFrame = None
        self.pose = pose
        self.currExercise = None
        self.features = defaultdict(int)
        self.hasBeenUp = False
        self.queue = []
        self.prediction = []
    id: str
    pose:any
    currFrame: str
    currExercise: str
    features: dict()
    hasBeenUp: bool
    queue: list
    prediction:any

connections = []


def startTime(connection):
    queueThread = threading.Thread(target=updateQueue, args=(connection,))
    queueThread.daemon = True
    queueThread.start()

    checkQueueThread = threading.Thread(target=updateFrames, args=(connection,))
    checkQueueThread.daemon = True
    checkQueueThread.start()



def updateQueue(connection):
    starttimes = time.time()
    while True:
        connection.queue.append(connection)
        time.sleep(0.04166 - ((time.time() - starttimes) % 0.04166))
        

def updateFrames(connection):
    while True:
        if(connection.queue):
            poseEstimation.receivedFrameData(connection.queue[0])
            connection.queue.pop(0)
        

def updateConnection (clientData):
    user = next(x for x in connections if x.id == clientData["id"])
    if(user):
        user.currFrame = clientData["frame"]
        user.currExercise = clientData["exerciseType"]

def getUser (id):
    return next(x for x in connections if x.id == id)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            if(data["type"] == "init"):
                connections.append(connectionUser(data["id"], mpPose.Pose()))
                connection = getUser(data["id"]);
                thread = threading.Thread(target=startTime, args=(connection,))
                thread.daemon = True
                thread.start()
            else:
                updateConnection(data)
                user = getUser(data["id"])
                if(user.prediction):
                    if(user.prediction[0] > 0.9):
                        await websocket.send_text("correct")
                        print("correct ", user.prediction[0])
                    else:
                        await websocket.send_text("incorrect")
                        print("incorrect ", user.prediction[0])
                    #print(json.dumps(user.prediction))
                    user.prediction = []

        except Exception as e:
            print("error: ", e)
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
