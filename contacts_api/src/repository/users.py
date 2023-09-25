from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.db.models import User
from src.schemas.users_schema import UserModel

async def get_user_by_email(email: str, db: Session) -> User | None:
    user = db.query(User).filter_by(email=email).first()
    return user

async def create_user(body: UserModel, db: Session):
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def update_token(user: User, refresh_token, db: Session):
    user.refresh_token = refresh_token
    db.commit()

async def change_password(email: str, new_password: str, db: Session):
    user = await get_user_by_email(email, db)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    user.password = pwd_context.hash(new_password)
    db.commit()

async def confirm_email(email: str, db: Session):
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email: str, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
