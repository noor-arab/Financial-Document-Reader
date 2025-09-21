from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os
import tempfile
from docx_parser import parse_docx
from chat_ner import parse_chat_ner

app = FastAPI(title="Financial Document Reader - Case Study")

@app.post("/upload/docx")
async def upload_docx(file: UploadFile = File(...)):
    """Process uploaded DOCX file and extract NER entities."""
    suffix = os.path.splitext(file.filename)[1].lower()
    if suffix != ".docx":
        raise HTTPException(status_code=400, detail="Please upload a DOCX file.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        entities = parse_docx(tmp_path)

        # Combine Party A and Party B into Counterparty if both exist
        if "Party A" in entities and "Party B" in entities:
            pa = entities.get("Party A", "")
            pb = entities.get("Party B", "")
            if pa or pb:
                entities["Counterparty"] = f"{pa}, {pb}"

    finally:
        os.remove(tmp_path)

    return JSONResponse(content=entities)


@app.post("/upload/chat")
async def upload_chat(file: UploadFile = File(...)):
    """Process uploaded chat/text file and extract NER entities."""
    suffix = os.path.splitext(file.filename)[1].lower()
    if suffix not in [".txt", ".chat", ".log"]:
        raise HTTPException(status_code=400, detail="Please upload a TXT/chat file.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            text = f.read()
        entities = parse_chat_ner(text)

    finally:
        os.remove(tmp_path)

    return JSONResponse(content=entities)
