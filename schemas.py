from pydantic import BaseModel 

class User(BaseModel):
    full_name: str
    email: str
    hashed_pw: str = ''
    password : str
    salary: float
    payment_info: str
    salt: str = None

class Login(BaseModel):
    email: str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    ip_address: str

