from fastapi import FastAPI, WebSocket
import uvicorn
import poseEstimation
import json
app = FastAPI(title='ESMA API')


class connection:
    def __init__(self, id):
        self.id = id
    id: str
    currFrame: str


connections = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            data = await websocket.receive_json()
            if(data["type"] == "init"):
                connections.append(connection(data["id"]))
            else:
                await poseEstimation.receivedFrameData(data["frame"])

        except Exception as e:
            print("error: ", e)
            break


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
