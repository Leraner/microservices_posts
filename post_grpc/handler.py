from post_microservice.database.dals import PostDAL
from post_microservice.database.database_conn import SingletonDatabaseConnection
from sqlalchemy.ext.asyncio import AsyncSession

from post_microservice.database.models import Post


class Handler(SingletonDatabaseConnection):
    @SingletonDatabaseConnection.create_session
    async def get_posts(self, db_session: AsyncSession):
        post_dal = PostDAL(db_session=db_session)
        return await post_dal.get_posts()

    @SingletonDatabaseConnection.create_session
    async def get_post_by_id(self, post_id: str, db_session: AsyncSession):
        post_dal = PostDAL(db_session=db_session)
        return await post_dal.get_post_by_id(post_id=post_id)

    @SingletonDatabaseConnection.create_session
    async def create_post(self, author_id: str, title: str, db_session: AsyncSession):
        post_dal = PostDAL(db_session=db_session)
        return await post_dal.create_post(author_id=author_id, title=title)

    @SingletonDatabaseConnection.create_session
    async def delete_post(self, post_id: str, db_session: AsyncSession):
        post_dal = PostDAL(db_session=db_session)
        await post_dal.delete_post(post_id=post_id)
