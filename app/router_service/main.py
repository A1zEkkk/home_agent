import os
from dotenv import load_dotenv

from router_service.client_model import LanguageModelClient
from router_service.prompt import router_prompt
from router_service.logger import setup_logging

from fastapi import FastAPI
from router_service.api.tasks import router, logging_middleware
#найти легковесную модель, которая позволит очень быстро поднимать и опускать роутинг

load_dotenv()
setup_logging()


client = LanguageModelClient(model_name=os.getenv("MODEL_NAME"), router_prompt=router_prompt())

app = FastAPI()

app.include_router(router)
app.middleware("http")(logging_middleware)