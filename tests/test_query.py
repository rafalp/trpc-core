import trpc


class Router(trpc.Router):
    @trpc.query
    def hello_world(context) -> str:
        return "Hello world"


server = trpc.Server(Router)


def test_server_query_returns_result():
    result = server.query("helloWorld")