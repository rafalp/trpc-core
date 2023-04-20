import trpc


class Router(trpc.Router):
    @trpc.query(name="helloWorld")
    def hello_world(context) -> str:
        return "Hello world"

    @trpc.mutation(name="sum")
    def sum(context, *, a: int, b: int) -> int:
        return a + b


server = trpc.Server(Router)


def test_server_query_returns_result():
    result = server.query("helloWorld")
    assert result == "Hello world"


def test_server_mutation_returns_result():
    result = server.mutation("sum", {"a": 1, "b": 3})
    assert result == 4
