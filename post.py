import grpc
from google.protobuf import wrappers_pb2
from sqlalchemy import select, delete

from db.engine import async_session
from db.models import User
from user_conn import get_users

protos, services = grpc.protos_and_services("protos/post_protos.proto")
user_protos, user_services = grpc.protos_and_services("protos/user_protos.proto")


class PostsService(services.PostsServicer):
    async def GetPosts(self, request, context):
        print("was here")
        response = await get_users()
        print(response)
        return protos.GetPostsResponse(
            posts=[
                protos.Post(
                    id="123",
                    title="123321",
                    user=user_protos.User(
                        id=response["id"],
                        name=response["name"],
                        surname=response["surname"],
                    ),
                )
            ]
        )
