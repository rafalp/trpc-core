`trpc-core`
===========

Toolkit for implementing tRPC servers in python

> `trpc-core` is currently in prototype stage. You are welcome to play with the code or drop feedback in issues, just don't expect anything usable or functional yet.


### Example tRPC API with Flask:

```python
import json

import trpc
from flask import Flask, jsonify, request


class Router(trpc.Router):
    @trpc.query(name="helloWorld")
    def hello_world(context) -> str:
        return "Hello world"

    @trpc.mutation(name="sum")
    def sum_items(context, *, a: int, b: int) -> int:
        return a + b


backend = trpc.Backend(Router)


app = Flask(__name__)


def batch_request():
    return request.args.get("batch") == "1"


def create_response(result: trcp.Result):
    return jsonify(result.data), result.status_code


@app.route("/trpc/<path:path>", methods=["GET"])
def trpc_query(path):
    if request.args.get("input"):
        input_data = json.loads(request.args["input"])
    else:
        input_data = None

    result = backend.query(
        path,
        batch=batch_request(),
        params=input_data,
        context=request,
    )
    return create_response(result)


@app.route("/trpc/<path:path>", methods=["POST"])
def trpc_mutation(path):
    result = backend.mutation(
        path,
        batch=batch_request(),
        params=request.get_json(),
        context=request,
    )
    return create_response(result)
```