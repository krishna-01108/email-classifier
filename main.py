from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
import pandas as pd
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

async def get_output(email_body):
    pipe=pickle.load(open('models/model.pkl', 'rb'))
    return  str(pipe.predict([email_body])[0])
# 1. Route to show the empty form
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# 2. Route to receive the submitted email body
@app.post("/submit-email", response_class=HTMLResponse)
async def handle_form(request: Request, email_body: str = Form(...)):
    # The 'email_body' variable matches the 'name' attribute in the HTML textarea
    result=await get_output(email_body)
    # Reload the page and pass a success message back to the template
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "result": result
        }
    )
