from datetime import date, datetime, timedelta
from typing import List

from fastapi import Depends, status, HTTPException, APIRouter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.db.db import get_db
from src.repository import contacts as repository_contacts
from src.schemas.contacts_schema import ContactModel, ContactResponse
from src.db.models import User
from src.services.auth import auth_service

from limiter import setup_limiter

router = APIRouter(prefix="/contacts", tags=['contacts'])

@router.on_event("startup")
async def startup():
    await setup_limiter()

@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def get_contacts(key: str = None, value: str = None, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(current_user.id, db)
    
    # birthday
    if key == 'birthday':
        
        today = datetime.now()
        days = today
        matching_contacts_by_birthday = []

        for _ in range(7):  
            for contact in contacts:
                birthday = contact.birthday

                if birthday.day == days.day and birthday.month == days.month:
                    matching_contacts_by_birthday.append(contact)

            days += timedelta(1)
        
        if not matching_contacts_by_birthday:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"From {today.date()} to {today.date() + timedelta(7)} nobody have the birthday!")

        return matching_contacts_by_birthday
    
    # first_name 
    elif key == 'first_name':
        matching_contacts_by_first_name = [contact for contact in contacts if str(contact.first_name).lower() == value.lower()]
        if not matching_contacts_by_first_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with first name '{value}' - not found!")
        return matching_contacts_by_first_name
    
    # last_name
    elif key == 'last_name':
        matching_contact_by_last_name = [contact for contact in contacts if str(contact.last_name).lower() == value.lower()]
        if not matching_contact_by_last_name:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with last name '{value}' - not found!")
        return matching_contact_by_last_name

    # phone
    elif key == 'phone':
        matching_contact_by_phone = [contact for contact in contacts if contact.phone == value]
        if not matching_contact_by_phone:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with phone '{value}' - not found!")
        return matching_contact_by_phone
    
    # email 
    elif key == 'email':
        matching_contact_by_email = [contact for contact in contacts if str(contact.email).lower() == value.lower()]
        if not matching_contact_by_email:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with email '{value}' - not found!")
        return matching_contact_by_email
    
    return contacts

@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def get_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user.id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id '{contact_id}' - not found!")
    return contact

@router.post('/', response_model=ContactResponse,  status_code=status.HTTP_201_CREATED, dependencies=[Depends(RateLimiter(times=3, seconds=5))], tags=['contacts'])
async def create_contact(body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(current_user.id, body, db)
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, current_user.id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} - not found!")
    return contact

@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user.id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact with id {contact_id} - not found!")
    return contact