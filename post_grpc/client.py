from typing import Any

import grpc
from google.protobuf.json_format import MessageToDict

from post_microservice.settings import microservices


class ClientInterface:
    client: Any
    protos: Any


class BaseClient:

    @classmethod
    def load_client(cls, microservice_info: dict):
        def wrapper(func):
            async def inner(*args, **kwargs):
                protos, services = grpc.protos_and_services(microservice_info["path_to_proto"])  # type: ignore
                channel = grpc.aio.insecure_channel(microservice_info["address"])
                stub_service_name = next(
                    filter(lambda x: "Stub" in x, services.__dict__)
                )
                client = services.__dict__[stub_service_name](channel)

                client_and_protos_object = ClientInterface()
                client_and_protos_object.__dict__.update(
                    {"client": client, "protos": protos}
                )
                return await func(*args, **kwargs, interface=client_and_protos_object)

            return inner

        return wrapper


class PostClient:
    """Class for communicating with others microservices"""

    @BaseClient.load_client(microservices["user"])
    async def get_user_by_id(self, user_id: str, interface: ClientInterface):
        response = await interface.client.GetUserById(
            interface.protos.GetUserByIdRequest(id=user_id), timeout=5
        )
        return MessageToDict(response)["user"]

    @BaseClient.load_client(microservices["user"])
    async def get_users_by_ids(self, user_ids: list[str], interface: ClientInterface):
        response = await interface.client.GetUsersByIds(
            interface.protos.GetUsersByIdsRequest(ids=user_ids), timeout=5
        )
        return MessageToDict(response)["users"]
