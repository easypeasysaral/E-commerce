from fastapi import APIRouter

router = APIRouter(prefix="/Products", tags=['Products API'])

fake_db = []

@router.get('/')
async def All_products(){
    return fake_db
}

