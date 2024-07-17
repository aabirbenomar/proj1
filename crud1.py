import mysql.connector
from mysql.connector import Error
from schemas import User
from security import generate_salt, get_password_hash, verify_password


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database='company',
            user='Proj',
            password='aaaa'
        
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_user(user: User):
    salt = generate_salt()
    hashed_pw = get_password_hash(user.password, salt)
    connection = create_connection()
    if connection is None:
        return {"error": "Unable to connect to database"}

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("""
            INSERT INTO USER (email, full_name, salary, payment_info, hashed_pw, salt)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user.email, user.full_name, user.salary, user.payment_info, hashed_pw, salt))
        connection.commit()
        return {"status": "User created successfully"}
    except Error as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

def get_user_by_email(email: str):
    connection = create_connection()
    if connection is None:
        return {"error": "Unable to connect to database"}

    cursor = connection.cursor(dictionary=True)
    try:
        #print(email)
        try:
            cursor.execute("SELECT * FROM USER WHERE email = %s", (email,))
        except Error as e:
            print(f"Error: {e}")
            return {"error": str(e)}
        result = cursor.fetchone()
        #print(user)
        if result:
            return result
        else:
            return {"error": "User not found"}
    except Error as e:
        print(f"Error: {e}")
        return {"error": str(e)}
    finally:
        cursor.close()
        connection.close()

def authenticate_user(email: str, password: str):
    result = get_user_by_email(email)
    #print(result)
    if "error" in result:
        return {"error": "Invalid email or password"}
    
    print(result)
    hashed_pw = result["hashed_pw"]
    if not verify_password(password, hashed_pw):
        return {"error": "Invalid email or password"}

    return result


