from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, auth, quiz, question, option, participant

origin = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class Route:
    def __init__(self, *args) -> None:
        [app.include_router(keys.router) for keys in args]


@app.get('/')
def root():
    return {'message': 'Welcome'}


app_route = Route(user, auth, quiz, question, option, participant)
