import trpc


class Router(trpc.Router):
    @trpc.query(name="helloWorld")
    def hello_world(context) -> str:
        return "Hello world"

    @trpc.mutation(name="sum")
    def sum(context, *, a: int, b: int) -> int:
        return a + b


backend = trpc.Backend(Router)


def test_backend_executes_query():
    result = backend.query("helloWorld")

    assert result.status_code == 200
    assert result.data == {
        "result": {
            "data": "Hello world",
        },
    }


def test_backend_executes_mutation():
    result = backend.mutation("sum", params={"a": 1, "b": 3})

    assert result.status_code == 200
    assert result.data == {
        "result": {
            "data": 4,
        },
    }
