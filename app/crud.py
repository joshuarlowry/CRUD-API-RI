from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas

# Create contact
async def create_contact(session: AsyncSession, contact_in: schemas.ContactCreate) -> models.Contact:
    new_contact = models.Contact(**contact_in.dict())
    session.add(new_contact)
    try:
        await session.commit()
        await session.refresh(new_contact)
    except IntegrityError as e:
        await session.rollback()
        raise
    return new_contact

# Get contact by id
async def get_contact(session: AsyncSession, contact_id: int) -> Optional[models.Contact]:
    result = await session.execute(select(models.Contact).where(models.Contact.id == contact_id))
    return result.scalar_one_or_none()

# Get all contacts
async def get_contacts(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Contact]:
    result = await session.execute(select(models.Contact).offset(skip).limit(limit))
    return result.scalars().all()

# Update a contact
async def update_contact(session: AsyncSession, contact_id: int, contact_in: schemas.ContactUpdate) -> Optional[models.Contact]:
    contact = await get_contact(session, contact_id)
    if not contact:
        return None

    for field, value in contact_in.dict(exclude_unset=True).items():
        setattr(contact, field, value)

    try:
        await session.commit()
        await session.refresh(contact)
    except IntegrityError:
        await session.rollback()
        raise
    return contact

# Delete contact
async def delete_contact(session: AsyncSession, contact_id: int) -> bool:
    contact = await get_contact(session, contact_id)
    if not contact:
        return False
    await session.delete(contact)
    await session.commit()
    return True 