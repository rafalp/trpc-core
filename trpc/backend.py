from dataclasses import dataclass

from typing import Any, Dict, List, Optional, Type, Union

from .procedure import Procedure, ProcedureType, WrappedProcedure
from .router import Router


class Backend:
    routers: List[Router]
    procedures: Dict[str, Union[Procedure, WrappedProcedure]]

    max_query: int
    max_mutation: int

    def __init__(
        self, *routers: Type[Router], max_query: int = 0, max_mutation: int = 0
    ):
        self.routers = []
        self.procedures = {}

        for router in routers:
            self.add_router(router)

        self.max_query = max_query
        self.max_mutation = max_mutation

    def add_router(self, router: Type[Router]):
        self.routers.append(router)

        for attr_name in dir(router):
            attr = getattr(router, attr_name)
            if isinstance(attr, (Procedure, WrappedProcedure)):
                self.procedures[attr.name] = attr

    def query(
        self,
        path: str,
        batch: bool = False,
        raw_input: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> "Result":
        return self.execute(
            ProcedureType.QUERY,
            path,
            batch,
            raw_input,
            context,
        )

    def mutation(
        self,
        path: str,
        batch: bool = False,
        raw_input: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> "Result":
        return self.execute(
            ProcedureType.MUTATION,
            path,
            batch,
            raw_input,
            context,
        )

    def execute(
        self,
        type_: ProcedureType,
        path: str,
        batch: bool = False,
        raw_input: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> "Result":
        if batch:
            return self.execute_batch(type_, path, raw_input, context)

        return self.execute_single(type_, path, raw_input, context)

    def execute_batch(
        self,
        type_: ProcedureType,
        path: str,
        raw_input: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> "Result":
        results = []
        status_codes = set()

        names = path.split(",")
        for i, call_name in enumerate(names):
            call_id = str(i)
            call_input = raw_input.get(call_id) if input else None
            result = self.execute_single(type_, call_name, call_input, context)

            results.append(result.data)
            status_codes.add(result.status_code)

        return Result(
            data=results,
            status_code=status_codes[0] if len(status_codes) == 1 else 207,
        )

    def execute_single(
        self,
        type_: ProcedureType,
        name: str,
        raw_input: Optional[Any] = None,
        context: Optional[Any] = None,
    ) -> "Result":
        procedure = self.procedures.get(name)
        if procedure is None or self.procedures[name].type_ != type_:
            raise Error(f'No "{str(type_).lower()}"-procedure on path "{name}"')

        if type_ == ProcedureType.QUERY:
            result = procedure.query(context, raw_input)
        elif type_ == ProcedureType.MUTATION:
            result = procedure.mutation(context, raw_input)

        return Result(
            data={
                "result": {
                    "data": result,
                },
            },
            status_code=200,
        )


@dataclass
class Result:
    data: Optional[Any]
    status_code: int


class Error(Exception):
    pass
