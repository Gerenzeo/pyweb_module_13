from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.db.models import Contact
from src.schemas.contacts_schema import ContactModel




async def get_contacts(user_id: int, db: Session):
    contacts = db.query(Contact).filter(Contact.contact_owner_id == user_id).all()
    return contacts

async def create_contact(user_id: int, body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    contact.contact_owner_id = user_id
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

async def get_contact_by_id(contact_id: int, user_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.contact_owner_id == user_id).first()
    return contact


async def update_contact(contact_id: int, user_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, user_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.birthday = body.birthday
        contact.email = body.email
        contact.phone = body.phone
        contact.favorite = body.favorite
        db.commit()
    return contact


async def remove_contact(contact_id:int, user_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, user_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
