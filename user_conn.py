import grpc
from google.protobuf.json_format import MessageToDict

protos, services = grpc.protos_and_services("protos/user_protos.proto")





async def get_users():
    print("get users")
    channel = grpc.aio.insecure_channel("0.0.0.0:50051")
    client = services.UsersStub(channel)
    response = await client.GetUsers(
        protos.GetUsersRequest(),
        timeout=5,
    )
    return MessageToDict(response)["users"][0]
    # print(MessageToDict(response))
