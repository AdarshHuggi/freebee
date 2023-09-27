from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models import model
from database.db_connection import Base,engine
from routers import user,auth,chat,file_upload


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(file_upload.router)


@app.get("/")
def root():
    return {"message": "Hello World pushing out to ubuntu"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)