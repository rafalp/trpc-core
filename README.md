`trpc-core`
===========

Toolkit for implementing tRPC servers in python

> `trpc-core` is currently in prototype stage. You are welcome to play with the code or drop feedback in issues, just don't expect anything usable or functional yet.


### Example tRPC API with Flask:

```python
import trpc
from flask import Flask, jsonify, request


class Router(trpc.Router):
    @trpc.query(name="helloWorld")
    def hello_world(context) -> str:
        return "Hello world"

    @trpc.mutation(name="sum")
    def sum(context, *, a: int, b: int) -> int:
        return a + b


server = trpc.Server(Router)


app = Flask(__name__)


@app.route("/trpc/<path:path>", methods=["GET"])
def trpc_query(path):
    result = server.query(path)
    return jsonify(result)


@app.route("/trpc/<path:path>", methods=["POST"])
def trpc_mutation(path):
    result = server.mutation(path)
    return jsonify(result)
```