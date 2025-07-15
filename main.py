from fastapi import FastAPI
from app.api.v2 import routes

app = FastAPI()

app.include_router(routes.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
