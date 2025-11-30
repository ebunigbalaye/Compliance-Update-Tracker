from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from app.InputValidation import UserForm
import os
from sendEmail.emailNew import *
import smtplib
from scraper.parse import *
from app_database import add_subscriber

app = FastAPI()

templates = Jinja2Templates(directory=r"C:\Users\pc\Documents\Compliance Update Tracker\app\html")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    # Initial empty data for form
    form_data = {"name":'', "email":''}

    return templates.TemplateResponse("templates.html", {"request": request, "form_data": form_data,"errors": {}})

@app.post("/", response_class=HTMLResponse)
async def submit_form(request: Request, name: str = Form(...), email: str = Form(...)):
    form_data = {"name": name, "email": email}
    try:
        # Validate form data using Pydantic
        user_data = UserForm(name=name, email=email)
        if not search_subscriber(email):
             add_subscriber(name,email)  
        else :
             return templates.TemplateResponse(
        "success.html",
        {"request": request, "data": user_data})
             
        with smtplib.SMTP_SSL('smtp.gmail.com',port=465) as my_gmail_server:
                # Getting email password
                password = os.getenv('gmail_access_key')
                my_gmail_server.login('ebunigbalaye@gmail.com',password)
                send_email(name,email,my_gmail_server)

         # If no validation errors, print a success message
        return templates.TemplateResponse(
        "success.html",
        {"request": request, "data": user_data})

    except ValidationError as e:
        error_dict = {}
        for err in e.errors():
            field = err['loc'][0]
            msg = err['msg']
            error_dict.setdefault(field, []).append(msg)
        # Pass validation errors to the template
        return templates.TemplateResponse("templates.html", {"request": request,"errors": error_dict, "form_data": form_data})
    
