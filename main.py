from fastapi import FastAPI, File, UploadFile
from process import ReturnInfoCard, MessageInfo, ExtractCardFront, ExtractCardBack
import json
import os
import cv2
import time
import shutil
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

class LimitUploadSize(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.method == 'POST':
            if 'content-length' not in request.headers:
                return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
            content_length = int(request.headers['content-length'])
            if content_length > self.max_upload_size:
                return Response(status_code=status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE)
        return await call_next(request)

app = FastAPI()
app.add_middleware(LimitUploadSize, max_upload_size=3000000)  # ~3MB

@app.get("/")
def read_root():
    return {"Hello": "Tan Dan SJC"}


@app.post("/CitizenIdentification/upload")
def upload(file: UploadFile = File(...)):
    try:
        pathSave = os.getcwd() + '\\anhcancuoc'
        if (os.path.exists(pathSave)):
            with open(f'anhcancuoc/{file.filename}','wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        else:
            os.mkdir(pathSave)
            with open(f'anhcancuoc/{file.filename}','wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        obj = ReturnInfoCard(f'anhcancuoc/{file.filename}')
        if (obj.type == "cccd_front"):
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data":[{"id": obj.id, "name": obj.name, "dob": obj.dob,"sex": obj.sex,
                    "nationality": obj.nationality,"home": obj.home, "address": obj.address, "doe": obj.doe,"imageFace": obj.imageFace, "type": obj.type}]}
        if (obj.type == "cccd_back"):
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data":[{"features": obj.features, "issue_date": obj.issue_date,
                    "type": obj.type}]}
        else:
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data": []}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}
