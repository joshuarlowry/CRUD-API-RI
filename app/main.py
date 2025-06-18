from typing import List
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .database import Base, engine, get_session

app = FastAPI(title="CRM API", version="1.0.0")

# Serve the simple HTML/JS test harness under /ui
frontend_path = Path(__file__).resolve().parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/ui", StaticFiles(directory=frontend_path, html=True), name="ui")


@app.on_event("startup")
async def on_startup() -> None:
    """Create database tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -------------------- CONTACT ENDPOINTS -------------------- #

@app.post(
    "/contacts",
    response_model=schemas.ContactOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"description": "Email already in use"},
    },
)
async def create_contact(
    contact_in: schemas.ContactCreate,
    session: AsyncSession = Depends(get_session),
):
    """Create a new contact."""
    try:
        contact = await crud.create_contact(session, contact_in)
        return contact
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A contact with this email already exists.",
        )


@app.get("/contacts", response_model=List[schemas.ContactOut])
async def list_contacts(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    """List contacts (paginated)."""
    contacts = await crud.get_contacts(session, skip=skip, limit=limit)
    return contacts


@app.get(
    "/contacts/{contact_id}",
    response_model=schemas.ContactOut,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found"}},
)
async def get_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    """Retrieve a single contact by ID."""
    contact = await crud.get_contact(session, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@app.put(
    "/contacts/{contact_id}",
    response_model=schemas.ContactOut,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found"}},
)
async def update_contact(
    contact_id: int,
    contact_in: schemas.ContactUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update an existing contact."""
    try:
        contact = await crud.update_contact(session, contact_id, contact_in)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        return contact
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already in use")


@app.delete(
    "/contacts/{contact_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Contact not found"}},
)
async def delete_contact(contact_id: int, session: AsyncSession = Depends(get_session)):
    """Delete a contact."""
    deleted = await crud.delete_contact(session, contact_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return None 