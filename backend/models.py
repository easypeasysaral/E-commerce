from sqlalchemy import Column, Integer, String, Boolean
from databases import Base

class DBproduct(Base):
    __tablename__ = "product"
    
    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String, index = True)
    product_name = Column(String, index = True)
    product_price = Column(Integer, index = True)
    product_availability = Column(Boolean, index = True)

