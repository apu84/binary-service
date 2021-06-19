from typing import List
from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse, Response, StreamingResponse
import aiofiles 
import mimetypes

app = FastAPI()
upload_directory = "/Users/apu/ExperimentLab/uploads/binary-service/"


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    for file in files:
        await save_file(file)

    return Response(content="{\"message\": \"File saved\"}", media_type="application/json", headers={"link": f"http://localhost:8000/files/{files[0].filename}"})


@app.get("/files/{file_name}")
def download_file(file_name):
    file = open(f"{upload_directory}{file_name}", "rb")
    mime_type = mimetypes.MimeTypes().guess_type(f"{upload_directory}{file_name}")[0]
    return StreamingResponse(file, media_type=mime_type) 


async def save_file(file):
    async with aiofiles.open(f'{upload_directory}{file.filename}', 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)


@app.get("/")
async def root():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
"""
    return HTMLResponse(content=content)
