from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import Login, Token, User ,TokenData
from crud1 import create_user, get_user_by_email, authenticate_user
from security import generate_salt
from fastapi.responses import JSONResponse
from verf import validate_email, validate_password


SECRET_KEY = 'your_secret_key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: str, ip_address: str, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'ip_address': ip_address})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get('/')
def index(request: Request):
    return JSONResponse(content={'message': f'Hello {request.client.host}'})


@app.post('/users/add')
def register_user(user: User):
    if not validate_email(user.email) :
        raise HTTPException(status_code=400, detail='Adresse email invalide.')
    elif validate_password(user.password):
        print("Compte creer  avec succès .")
    else :
        raise HTTPException(status_code=400, detail='Mot de passe doit avoir au moins 8 charactere et des chiffres aussi des lettres majuscules et minuscule . reessayer !.')
 
    user.salt = generate_salt()
    success = create_user(user)
    if not success:
        raise HTTPException(status_code=400, detail='Email already registered')
    return {'success': success, 'full_name': user.full_name, 'email': user.email, 'salary': user.salary, 'payment_info': user.payment_info}


@app.post('/login', response_model=Token)
def login(user: Login, request: Request):
    client_ip = request.client.host
    user_data = authenticate_user(user.email, user.password)
    if "error" in user_data:
        raise HTTPException(status_code=401, detail=user_data["error"], headers={'WWW-Authenticate': 'Bearer'})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'email': user_data['email']}, ip_address=client_ip, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer', 'email': user_data['email'], 'ip_address': client_ip}

def get_token_data(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('email')
        ip_address = payload.get('ip_address')
        if not email:
            raise JWTError
        return TokenData(email=email, ip_address=ip_address)
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
@app.get('/users/me/')
def read_user_salary(request: Request, token: str = Depends(oauth2_scheme)):
    token_data = get_token_data(token)
    user = get_user_by_email(email=token_data.email)
    if "error" in user:
        raise HTTPException(status_code=404, detail=user["error"])

    client_ip = request.client.host
    if token_data.ip_address != client_ip:
        raise HTTPException(status_code=401, detail='Token IP address does not match the client IP', headers={'WWW-Authenticate': 'Bearer'})

    return {"salary": user["salary"]}



