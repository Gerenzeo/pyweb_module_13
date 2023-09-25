from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from src.db.db import get_db
from src.schemas.email_schema import RequestEmail
from src.schemas.users_schema import UserModel, UserResponse
from src.schemas.tokens_schema import TokenModel
from src.repository.users import create_user, get_user_by_email, update_token, confirm_email, change_password
from src.services.auth import auth_service
from src.services.email_service import send_email, reset_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    exist_user = await get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Account with email {exist_user.email} already exist!")

    body.password = auth_service.get_password_hash(body.password)
    new_user = await create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user

@router.post('/login', response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    unauthorizedExc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password!")
    user = await get_user_by_email(body.username, db)
    if user is None:
        raise unauthorizedExc
    if not auth_service.verify_password(body.password, user.password):
        raise unauthorizedExc
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db)

    if user.email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await confirm_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    user = await get_user_by_email(body.email, db)
    if user:
        if user.confirmed:
            return {"message": "Your email is already confirmed"}
        background_tasks.add_task(send_email, user.email, user.username, str(request.base_url))
    return {"message": "Check your email for confirmation."}

# # ###
# @router.post('/request_reset_password')
# async def request_reset_password(body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
#     user = await get_user_by_email(body.email, db)
#
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found!')
#
#     background_tasks.add_task(reset_password, user.email, user.username, str(request.base_url))
#     return {"message": "We send new password on your email!"}
# # ###

@router.post('/request_reset_password')
async def request_reset_password(body: RequestEmail, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    user = await get_user_by_email(body.email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found!')

    background_tasks.add_task(reset_password, user.email, user.username, str(request.base_url))
    return {"message": "We send new password on your email!"}

@router.get('/set_new_password/{token}')
async def set_new_password(token: str, new_password: str, confirm_new_password: str, db: Session = Depends(get_db)):
    email = auth_service.get_email_from_token(token)
    user = await get_user_by_email(email, db)

    if user.email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    if not new_password == confirm_new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords not same")

    await change_password(email, new_password, db)
    return {"message": "Password successfully changed"}


