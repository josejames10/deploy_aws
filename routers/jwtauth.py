from fastapi import APIRouter,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime,timedelta

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})
ACCESS_TOKEN_EXPIRE = 1
ALGORITHM = "HS256"
SECRET= "dc40e95b3f6c7850281d32ec29277079e106ace5c9e835ee6ffbc1eda477e43f"

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2=OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "braismoure@mourede.com",
        "disabled": False,
        "password": "$2a$12$LwVBLqqS2GVKvmxy1UsI7.jXHp0qNq2ZFq5./C8x.lpfpoxigeQr6"
    },
    "mouredev2": {
        "username": "mouredev2",
        "full_name": "Brais Moure 2",
        "email": "braismoure2@mourede.com",
        "disabled": True,
        "password": "$2a$12$ux1FHzns9L7pKIzIY4O5L.Hj9CsF.aoaxrNpIFkK8YQUUwNFCJ.TS"
    }
}
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)


async def current_user(user:User=Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm=Depends()):
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="usuario no encontrado")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400,detail="usuario no encontrado")
    access_token={"sub":user.username,"exp":datetime.utcnow()+timedelta(minutes=(ACCESS_TOKEN_EXPIRE))}                              
    
    return {"access_token":jwt.encode(access_token,SECRET,algorithm=ALGORITHM), "token_type" : "bearer"}


@router.get("/users/me")
async def me(user : User = Depends(current_user)):
    return user
