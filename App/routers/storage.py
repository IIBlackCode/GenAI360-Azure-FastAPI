from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from azure.storage.blob import BlobServiceClient

templates = Jinja2Templates(directory="templates")
router = APIRouter()

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=kmsgenai360st;AccountKey=GfnbYOozbGdVfwd/Ds4YGnBifn6WnP8x5JIH12NI9Am4mhDIH+ko7ndW68gsdYmiMMSyfxvNqH/9+AStWRdGUw==;EndpointSuffix=core.windows.net"
AZURE_CONTAINER_NAME = "pdf"
# Azure Blob Service Client 초기화
# blob_service_client = BlobServiceClient.from_connection_string(os.getenv(AZURE_STORAGE_CONNECTION_STRING))
# container_name = os.getenv(AZURE_CONTAINER_NAME)


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if AZURE_STORAGE_CONNECTION_STRING:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    else:
        raise ValueError("Connection string is empty or None")
    
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        # Blob 클라이언트 초기화
        blob_client = blob_service_client.get_blob_client(container=AZURE_CONTAINER_NAME, blob=file.filename)

        # 파일 업로드
        blob_client.upload_blob(file.file, blob_type="BlockBlob")

        return {"filename": file.filename, "status": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files/")
async def list_files():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client("pdf")
        blob_list = container_client.list_blobs()
        files = [{"name": blob.name} for blob in blob_list]
        print(files)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))