import numpy as np
import cv2 as cv
import base64

fps = 100 #amount of miliseconds to wait, before showing next image

async def receivedFrameData(bytes:str):
    img = await decodeBase64(bytes)
    await showFrame(img, fps)

async def showFrame(frame:np.mat, fps:int):
    cv.imshow("img",frame)
    cv.waitKey(fps)

async def decodeBase64(bytes:str):
    im_bytes = base64.b64decode(bytes)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
    return img