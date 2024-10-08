from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from ai import OpenAI
from ai.Azure import Gpt4omini, Gpt4o, Gpt4o_addData

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/tset/{question}")
def test(question: str):
    # result = OpenAI.chatgpt(question)
    result = ''
    return {"message": result}

@router.get("/key/{key}")
def key(key: str):
    result = OpenAI.apikey(key)
    return {"result": result}

@router.get("/apitest/{question}")
def test(question: str):
    result = OpenAI.apitest(question)
    return {"message": result}

@router.get("/openai/{question}")
def test(question: str):
    result = OpenAI.chatgpt(question)
    return {"message": result}

@router.get("/gpt4o/{question}")
def gpt4o(question: str):
    result = Gpt4o.run(question)
    return {"message": result}

@router.get("/gpt4omini/{question}")
def gpt4omini(question: str):
    result = Gpt4omini.run(question)
    return {"message": result}

@router.get("/gpt4o_addData/{question}")
def gpt4o(question: str):
    result = Gpt4o_addData.run(question)
    return {"message": result}