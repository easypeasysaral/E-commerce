from fastapi import APIRouter,HTTPException, Depends
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session
from databases import get_db
import models

router = APIRouter(prefix="/Products", tags=['Products API'])

class Product(BaseModel):
    
    product_type : str = Field(...,description="This is the type of product")
    product_price : int = Field(...,description="This is the product price")
    product_name : str = Field(...,description="This is the name of the product")
    product_availability : bool = Field(default=True,description="This shows the availability of the product")
    

@router.get('/')
async def all_product(db : Session = Depends(get_db)):
        products = db.query(models.DBproduct).all()
        return products


@router.get('/{product_id}')
async def get_product(product_id : int, db: Session = Depends(get_db)):
    product = db.query(models.DBproduct).filter(models.DBproduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with product_id {product_id} is not found")

    return product

@router.post('/')
async def add_product(product : Product, db: Session = Depends(get_db)):
    new_product = models.DBproduct(
         product_type=product.product_type,
        product_name=product.product_name,
        product_price=product.product_price,
        product_availability=product.product_availability
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return {
        'message':"Data uploaded successfully to Neon Db",
        'data':new_product
    }
    


@router.delete('/{product_id}')
async def delete_product(product_id : int, db:Session = Depends(get_db)):
    product =  db.query(models.DBproduct).filter(models.DBproduct.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail= f"Product with product_id {product_id} is not found")
    
    db.delete(product)
    db.commit()
    
    return{
        'message' : f"Product {product_id} deleted successfully"
    } 
    

    
@router.put('/{product_id}')
async def update_product(product_id : int,product_data : Product, db:Session = Depends(get_db)):
    product_in_db = db.query(models.DBproduct).filter(models.DBproduct.id == product_id).first()
    
    if not product_in_db:
        raise HTTPException(status_code=404, detail = f"Product with product_id {product_id} is not found")
    
    product_in_db.product_type = product_data.product_type
    product_in_db.product_name = product_data.product_name
    product_in_db.product_price = product_data.product_price
    product_in_db.product_availability = product_data.product_availability
    
    db.commit()
    db.refresh(product_in_db)
    
    return {
        "message" : "Product updated successfully",
        "data" : product_in_db
    }
    

    