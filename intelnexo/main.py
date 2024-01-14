from controllers.paypal import create_url
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from controllers.db import users
SECRET_KEY =getenv("SECRET_KEY")
ALGORITHM =getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("EXPIRE"))
load_dotenv()

# Se crean los modelos para el manejo del api

class TokenData(BaseModel):
    username: Union[str, None] = None
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    disabled: Union[bool, None] = None
class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compara la password creada y la que se encuentra almacenada del usuario.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Genera un hash con la password ingresada por el usuario

def get_password_hash(password):
    return pwd_context.hash(password)

# Busca si existe el usuario dentro de la base de datos
def get_user(db, username: str):
    for user in db:
        if user['username'] == username:
            user_dict = user
            return UserInDB(**user_dict)

# valida la existencia del usuario según el usuario y contraseña ingresados
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Genera un token valido durante x tiempo en minutos según la variable EXPIRE ubicada en .env
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verifica la veracidad el token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Posibilidad de deshabilitar el acceso a usuarios
async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Representación temporal para el comiendo de manejo de usuarios, permitiendo agregar un nuevo usuario que pueda generar
# tokens y poder usar el generador de urls para pagos con paypal

@app.post("/register")
def sign_in_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users.append({"username": form_data.username, "hashed_password":pwd_context.hash(form_data.password), "disabled":False})
    return "User Created"

# Genera un enpoint, el cual sigue el formulario normal de fastapi, en el cual es relevante el usurname y la password,
# en este caso se usa prueba y prueba respectivamente, este nos devolvera access_token y el tipo de token

@app.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

# Endpoint que genera el link de pago, se declara current_user para el tema de seguridad, se puede utilizar en un
# futuro para generar trazabilidad.

@app.post("/generate")
async def generate_link(mount: float, current_user: Annotated[User, Depends(get_current_active_user)]):
    return create_url(mount)