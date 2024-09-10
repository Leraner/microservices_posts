from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Post
from uuid import UUID


class PostDAL:
    """Data Access Layer for operating post info"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_posts(self):
        query = select(Post)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def get_post_by_id(self, post_id: str):
        query = select(Post).where(Post.id == post_id)
        result = await self.db_session.execute(query)
        row = result.fetchone()
        if row is not None:
            return row[0]

    async def create_post(self, author_id: str, title: str):
        new_post = Post(author_id=UUID(author_id), title=title)
        self.db_session.add(new_post)
        await self.db_session.flush()
        await self.db_session.refresh(new_post)
        return new_post

    async def delete_post(self, post_id: str):
        query = delete(Post).where(Post.id == post_id).returning(Post)
        result = await self.db_session.execute(query)
        rows = result.fetchone()

        if rows is not None:
            return rows[0]
