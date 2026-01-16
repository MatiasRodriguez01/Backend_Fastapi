from db.modules.base_module import Base

class Product(Base):
    name: str
    price: int 
    stock: int

