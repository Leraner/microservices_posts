import grpc
from post_microservice.post_grpc.post import PostsService
from settings import microservices

protos, services = grpc.protos_and_services("protos/post_protos.proto")


async def run_server():
    server = grpc.aio.server()
    services.add_PostsServicer_to_server(PostsService(), server)
    address = microservices["post"]["address"]
    server.add_insecure_port(address)
    print("Service started on 0.0.0.0:50052")
    await server.start()
    await server.wait_for_termination()
