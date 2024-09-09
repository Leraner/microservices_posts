import grpc
from post import PostsService

protos, services = grpc.protos_and_services("protos/post_protos.proto")


async def run_server():
    server = grpc.aio.server()
    services.add_PostsServicer_to_server(PostsService(), server)
    server.add_insecure_port("0.0.0.0:50052")
    print("Service started on 0.0.0.0:50052")
    await server.start()
    await server.wait_for_termination()
