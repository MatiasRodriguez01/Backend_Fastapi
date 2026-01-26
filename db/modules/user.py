from db.modules.base_module import Base 


class User(Base):
    id: str = ""
    username: str
    password: str
    email: str
    age: int

