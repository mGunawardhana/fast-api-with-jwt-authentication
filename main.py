import uvicorn
from fastapi import FastAPI, Body, Depends
from app.model import PostSchema
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import sign_jwt
from app.auth.jwt_bearer import jwtBearer

posts = [{"id": 1, "title": "penguins 🐧", "text": "Penguins are a group of aquatic flightless birds."},
         {"id": 2, "title": "tigers 🐯",
          "text": "Tigers are the largest living cat species and a members of the genus Panthers."},
         {"id": 3, "title": "koalas 🐨", "text": "Koala is arboreal herbivorous marsupial native to Australia ."}, ]

users = []

app = FastAPI()


@app.get("/", tags=["test"])
async def greet():
    return {"Hello": "World"}


@app.get("/posts", tags=["test"])
async def get_posts():
    return {"data": posts}


@app.get("posts/{id}", tags=["posts"])
async def find_by_id(id: int):
    if id > len(posts):
        return {"error": "id does not exists"}

    for post in posts:
        if post["id"] == id:
            return {"data": post}


@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["posts"])
async def save_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {"info": "Save Success!", "data": post}


@app.post("/user/signup", tags=["user"])
async def signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return sign_jwt(user.email)


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


@app.post("/user/login", tags=["user"])
async def login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return sign_jwt(user.email)
    return {"error": "Wrong credentials"}
