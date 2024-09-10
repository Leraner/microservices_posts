from uuid import uuid4

import grpc

from .client import PostClient
from .handler import Handler

protos, services = grpc.protos_and_services("protos/post_protos.proto")
user_protos, user_services = grpc.protos_and_services("protos/user_protos.proto")


class PostsService(services.PostsServicer, Handler, PostClient):
    async def GetPosts(self, request, context):
        posts = await self.get_posts()
        post_authors = await self.get_users_by_ids(
            user_ids=[str(post.author_id) for post in posts]
        )

        posts_and_posts_authors = [
            {
                "post": post,
                "author": next(
                    filter(lambda x: x["id"] == str(post.author_id), post_authors),
                    {"id": str(uuid4()), "name": "Deleted", "surname": "Deleted"},
                ),
            }
            for post in posts
        ]

        response = protos.GetPostsResponse(
            posts=[
                protos.Post(
                    id=str(data["post"].id),
                    title=data["post"].title,
                    user=user_protos.User(
                        id=data["author"]["id"],
                        name=data["author"]["name"],
                        surname=data["author"]["surname"],
                    ),
                )
                for data in posts_and_posts_authors
            ]
        )

        return response

    async def GetPostById(self, request, context):
        post = await self.get_post_by_id(post_id=request.id)

        if post is None:
            raise Exception(f"No post with id: {request.id}")

        post_author = await self.get_user_by_id(user_id=str(post.author_id))

        if post_author is None:
            post_author = {
                "id": str(uuid4()),
                "name": "Deleted",
                "surname": "Deleted",
            }

        response = protos.GetPostByIdResponse(
            post=protos.Post(
                id=str(post.id),
                title=post.title,
                user=user_protos.User(
                    id=post_author["id"],
                    name=post_author["name"],
                    surname=post_author["surname"],
                ),
            ),
        )
        return response

    async def CreatePost(self, request, context):
        post_author = await self.get_user_by_id(user_id=request.author_id)
        post = await self.create_post(author_id=request.author_id, title=request.title)

        if post_author is None:
            post_author = {
                "id": str(uuid4()),
                "name": "Deleted",
                "surname": "Deleted",
            }

        response = protos.CreatePostResponse(
            post=protos.Post(
                id=str(post.id),
                title=post.title,
                user=user_protos.User(
                    id=post_author["id"],
                    name=post_author["name"],
                    surname=post_author["surname"],
                ),
            )
        )

        return response

    async def DeletePost(self, request, context):
        deleted_post = await self.delete_post(post_id=request.id)

        if deleted_post is None:
            raise Exception(f"No post with id: {request.id}")

        post_author = await self.get_user_by_id(user_id=deleted_post.author_id)

        if post_author is None:
            post_author = {
                "id": str(uuid4()),
                "name": "Deleted",
                "surname": "Deleted",
            }

        response = protos.DeletePostResponse(
            post=protos.Post(
                id=str(deleted_post.id),
                titile=deleted_post.title,
                user=user_protos.User(
                    id=post_author["id"],
                    name=post_author["name"],
                    surname=post_author["surname"],
                ),
            )
        )

        return response
