import bcrypt

def generate_salt():
    salt = bcrypt.gensalt(rounds=15)
    return salt

def get_password_hash(password, salt):
    bpassword = bytes(password, 'utf-8')
    hashed_password = bcrypt.hashpw(bpassword, salt)
    return hashed_password

def verify_password(plain_password:str, hashed_password_db:str):
    bhashed_password = bytes(hashed_password_db, 'utf-8')
    bplain_password = bytes(plain_password, 'utf-8')
    equals = bcrypt.hashpw(bplain_password, bhashed_password)
    
    return equals
  