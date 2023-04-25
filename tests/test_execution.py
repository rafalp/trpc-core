import trpc


class Router(trpc.Router):
    @trpc.query(name="helloWorld")
    def hello_world(context) -> str:
        return "Hello world"

    @trpc.mutation(name="clearCache")
    def clear_cache(context) -> bool:
        return True

    @trpc.mutation(name="add")
    def add(context, a: int, b: int) -> int:
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


def test_backend_executes_mutation_without_input():
    result = backend.mutation("clearCache")

    assert result.status_code == 200
    assert result.data == {
        "result": {
            "data": True,
        },
    }


def test_backend_executes_mutation_with_input():
    result = backend.mutation("add", raw_input=(3, 4))

    assert result.status_code == 200
    assert result.data == {
        "result": {
            "data": 7,
        },
    }
