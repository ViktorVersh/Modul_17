from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/all_products")
async def get_all_products():
    pass


@router.post("/create")
async def creaty_product():
    pass


@router.put("/update_product")
async def update_product():
    pass


@router.delete("/delete")
async def delete_product():
    pass
