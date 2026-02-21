import os
from dotenv import load_dotenv

from . import client_model
from . import prompt
from logger import setup_logging

from fastapi import FastAPI
from app.router_service.api.tasks import router, logging_middleware
#найти легковесную модель, которая позволит очень быстро поднимать и опускать роутинг

load_dotenv()
setup_logging()


client = client_model.LanguageModelClient(model_name=os.getenv("MODEL_NAME"), router_prompt=prompt.router_prompt())

app = FastAPI()

app.include_router(router)
app.middleware("http")(logging_middlewgiare)