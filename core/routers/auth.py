from datetime import timedelta, datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from core.models import User
from core.schemas import UserRegister, TokenResponse
from env_config import SessionLocal, ALGORITHM, SECRET_KEY

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses={401: {'user': 'Not authorized'}}
)


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {'sub': username, 'id': user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user_role_from_database(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return user.role
    return None


async def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role = await get_user_role_from_database(db, username)

        if username is None or user_id is None or role is None:
            raise get_user_exception()
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise get_user_exception()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_register: UserRegister, db: Session = Depends(get_db)):
    if user_register.role not in ['admin', 'user']:
        raise HTTPException(status_code=400, detail="Invalid role. Allowed roles are 'admin' or 'user'")
    user_registration_model = User(
        email=user_register.email,
        username=user_register.username,
        first_name=user_register.first_name,
        last_name=user_register.last_name,
        role=user_register.role,
        hashed_password=bcrypt_context.hash(user_register.password),
        is_active=True
    )
    db.add(user_registration_model)
    db.commit()


@router.post("/token", response_model=TokenResponse)
async def login_user_with_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                db: Session = Depends(get_db)):
    user: User = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validation credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Incorrect username or password',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    return token_exception_response
