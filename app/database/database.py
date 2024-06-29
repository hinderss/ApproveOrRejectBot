from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from app.database.models import Review, Reviewed, User

Base = declarative_base()


class Database:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)
        print("The database is connected successfully")

    async def add_review(self, document_id, user_id, chat_msg_id, admin_msg_id):
        async with self.Session() as session:
            async with session.begin():
                try:
                    review = Review(document_id=document_id,
                                    user_id=user_id,
                                    chat_msg_id=chat_msg_id,
                                    admin_msg_id=admin_msg_id
                                    )
                    session.add(review)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print("DB query error:", e)
                    raise

    async def add_user(self, user_id, name, language='en'):
        async with self.Session() as session:
            async with session.begin():
                try:
                    user = User(user_id=user_id, name=name, language=language)
                    await session.merge(user)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print("DB query error:", e)
                    raise

    async def get_users(self):
        async with self.Session() as session:
            async with session.begin():
                result = await session.execute(select(User))
                return result.scalars().all()

    async def increment_user_sent(self, user_id):
        async with self.Session() as session:
            async with session.begin():
                user = (await session.execute(select(User).filter_by(user_id=user_id))).scalars().first()
                if user:
                    user.sent += 1
                    await session.commit()

    async def increment_user_accepted(self, user_id):
        async with self.Session() as session:
            async with session.begin():
                user = (await session.execute(select(User).filter_by(user_id=user_id))).scalars().first()
                if user:
                    user.accepted += 1
                    await session.commit()

    async def decrement_user_accepted(self, user_id):
        async with self.Session() as session:
            async with session.begin():
                user = (await session.execute(select(User).filter_by(user_id=user_id))).scalars().first()
                if user:
                    user.accepted -= 1
                    await session.commit()

    async def get_user(self, user_id):
        async with self.Session() as session:
            async with session.begin():
                result = await session.execute(select(User).filter_by(user_id=user_id))
                return result.scalars().first()

    async def get_reviewed_msg_id(self, user_id, chat_msg_id):
        async with self.Session() as session:
            async with session.begin():
                reviewed = (await session.execute(select(Reviewed).filter_by(user_id=user_id,
                                                                             chat_msg_id=chat_msg_id
                                                                             ))).scalars().first()
                return reviewed.reviewed_msg_id if reviewed else None

    async def update_feedback(self, user_id, chat_msg_id, feedback):
        async with self.Session() as session:
            async with session.begin():
                reviewed = (await session.execute(select(Reviewed).filter_by(user_id=user_id,
                                                                             chat_msg_id=chat_msg_id
                                                                             ))).scalars().first()
                if reviewed:
                    reviewed.feedback = feedback
                    await session.commit()

    async def add_reviewed(self, user_id, chat_msg_id, reviewed_msg_id, accepted, feedback=None):
        async with self.Session() as session:
            async with session.begin():
                try:
                    review = (await session.execute(
                        select(Review).filter_by(user_id=user_id, chat_msg_id=chat_msg_id)
                    )).scalars().first()
                    if review:
                        document_id = review.document_id
                    else:
                        document_id = None
                    reviewed = Reviewed(document_id=document_id,
                                        user_id=user_id,
                                        chat_msg_id=chat_msg_id,
                                        reviewed_msg_id=reviewed_msg_id,
                                        accepted=accepted,
                                        feedback=feedback
                                        )
                    session.add(reviewed)
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print("DB query error:", e)
                    raise

    async def get_document_accepted(self, user_id, chat_msg_id):
        async with self.Session() as session:
            async with session.begin():
                reviewed = (await session.execute(select(Reviewed).filter_by(user_id=user_id,
                                                                             chat_msg_id=chat_msg_id
                                                                             ))).scalars().first()
                return reviewed.accepted if reviewed else None

    async def update_accepted(self, accepted, user_id, chat_msg_id):
        async with self.Session() as session:
            async with session.begin():
                reviewed = (await session.execute(select(Reviewed).filter_by(user_id=user_id,
                                                                             chat_msg_id=chat_msg_id
                                                                             ))).scalars().first()
                if reviewed:
                    reviewed.accepted = accepted
                    await session.commit()

    async def update_language(self, user_id, language):
        async with self.Session() as session:
            async with session.begin():
                user = (await session.execute(select(User).filter_by(user_id=user_id))).scalars().first()
                if user:
                    user.language = language
                    await session.commit()

    async def clear_all_tables(self):
        async with self.Session() as session:
            async with session.begin():
                try:
                    await session.execute(delete(Review))
                    await session.execute(delete(Reviewed))
                    await session.execute(delete(User))
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print("DB query error:", e)
                    raise

    async def clear_tables_zero_users(self):
        async with self.Session() as session:
            async with session.begin():
                try:
                    await session.execute(delete(Review))
                    await session.execute(delete(Reviewed))
                    await session.execute(update(User).values(sent=0, accepted=0))
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print("DB query error:", e)
                    raise
