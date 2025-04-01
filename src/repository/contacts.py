from datetime import timedelta
from typing import List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.contact import Contact
from src.schemas.contact import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_contacts(
        self,
        skip: int = 0,
        limit: int = 100,
        q: str | None = None,
    ) -> List[Contact]:
        stmt = select(Contact)
        if q:
            stmt = stmt.filter(
                Contact.first_name.contains(q)
                | Contact.last_name.contains(q)
                | Contact.email.contains(q)
            )
        stmt = stmt.offset(skip).limit(limit)

        contacts = await self.session.execute(stmt)
        return contacts.scalars().all()

    async def get_contact(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        contact = await self.session.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel
    ) -> Contact | None:
        contact = await self.get_contact(contact_id)
        if contact:
            for key, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, key, value)
            await self.session.commit()
            await self.session.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> None:
        contact = await self.get_contact(contact_id)
        if contact:
            await self.session.delete(contact)
            await self.session.commit()
        return contact

    async def get_birthdays(self, days: int) -> List[Contact]:
        stmt = select(Contact).where(
            Contact.date_of_birth.between(
                func.current_date(),
                func.current_date() + timedelta(days=days),
            )
        )
        contacts = await self.session.execute(stmt)
        return contacts.scalars().all()
