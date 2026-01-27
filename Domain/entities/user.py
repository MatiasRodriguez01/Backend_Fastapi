class User:
    def __init__(self, 
                 username: str, 
                 password: str, 
                 email: str, 
                 age: int,
                 id: str | None = None):
        if "@" not in email:
            raise ValueError("Email inválido")
        if age < 0:
            raise ValueError("La edad no puede ser negativa")
        
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.age = age