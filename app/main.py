from fastapi import FastAPI
from routers import category
from routers import products


app = FastAPI()


@app.get('/')
async def welcome():
    return {"message": 'My e-commerce app'}

app.include_router(category.router)
app.include_router(products.router)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',
                host='127.0.0.1',
                port=8000,
                reload=True)
