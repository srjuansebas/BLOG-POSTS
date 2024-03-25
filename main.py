from fastapi import FastAPI
from routers import users, login



app = FastAPI()


app.include_router(users.router)
app.include_router(login.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido a tu BLOG"}

