from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field

router = APIRouter(prefix="/Products", tags=['Products API'])

fake_db = []

class Product(BaseModel):
    product_id : int = Field(...,description="This is the id of the product")
    product_type : str = Field(...,description="This is the type of product")
    product_price : int = Field(...,description="This is the product price")
    product_name : str = Field(...,description="This is the name of the product")
    product_availability : bool = Field(default=True,description="This shows the availability of the product")
    

@router.get('/')
async def all_product():
    return fake_db


@router.get('/{product_id}')
async def get_product(product_id : int):
    for product in fake_db:
        if product.product_id == product_id:
            return product
    
    raise HTTPException(status_code=404, detail="Invalid product_id")

@router.post('/')
async def add_product(product : Product):
    fake_db.append(product)
    
    return {
        'message' : "Data uploaded successfully",
        'data' : product
    }


@router.delete('/{product_id}')
async def delete_product(product_id : int):
    for product in fake_db:
        if product.product_id == product_id:
            fake_db.remove(product)
            return{
                'message' : f"Product with {product_id} deleted successfullly",
            }
    
    raise HTTPException(status_code=404, detail=f"Product with {product_id} not found")


    
@router.put('/{product_id}')
async def update_product(product_id : int,product : Product):
    for pro in fake_db:
        if pro.product_id == product_id:
            pro.product_type = product.product_type
            pro.product_name = product.product_name
            pro.product_price = product.product_price
            pro.product_availability = product.product_availability
            
            break
    
    raise HTTPException(status_code=404, detail=f"Product with {product_id} not found")

    