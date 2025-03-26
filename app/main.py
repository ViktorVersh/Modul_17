from fastapi import FastAPI
from routers import category


app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": 'My shop'}

app.include_router(category.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',
                port=8000,
                host='127.0.0.1',
                reload=True)
