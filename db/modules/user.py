from db.modules.base_module import Base 

class User(Base):
    name: str
    email: str
    url: str