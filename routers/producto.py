from fastapi import APIRouter

router = APIRouter()

producto=["producto1","producto2"]

@router.get("/producto")
async def read_producto():
    return producto