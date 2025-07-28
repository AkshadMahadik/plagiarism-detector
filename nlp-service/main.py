from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from utils.extract import extract_text
from utils.similarity import get_similarity_score

app = FastAPI()

# Allow CORS for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "NLP service is running!"}

@app.post("/analyze/")
async def analyze(files: List[UploadFile] = File(...)):
    if len(files) != 2:
        return {"error": "Please upload exactly two files"}
    
    texts = []
    for file in files:
        content = await file.read()
        text = extract_text(file.filename, content)
        texts.append(text)

    score = get_similarity_score(texts[0], texts[1])
    return {"similarity": round(score * 100, 2)}
