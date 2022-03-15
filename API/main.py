from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Optional
import poseEstimation

class Data(BaseModel):
    byteData:Optional[str] = None;

app = FastAPI()


@app.post("/")
async def queryLemma(data: Data):
    await poseEstimation.receivedFrameData(data.byteData);
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)