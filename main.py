from fastapi import FastAPI
from routers import producto,user
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.include_router(producto.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}   