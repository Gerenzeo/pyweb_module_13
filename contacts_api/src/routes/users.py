from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from src.db.db import get_db
from src.db.models import User
from src.schemas.users_schema import UserResponse
from src.services.auth import auth_service
from src.services.cloudinary_service import CloudImage
from src.repository.users import update_avatar

router = APIRouter(prefix="/users", tags=['users'])

@router.get("/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user

@router.put('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    public_id = CloudImage.genereate_name_avatar(current_user.email)
    r = CloudImage.upload(file.file, public_id)
    src_url = CloudImage.get_url_for_avatar(public_id, r)
    user = await update_avatar(current_user.email, src_url, db)
    return user

