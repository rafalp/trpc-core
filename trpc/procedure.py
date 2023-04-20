from enum import Enum
from typing import Callable, Optional, overload


class ProcedureType(str, Enum):
    MUTATION = "mutation"
    QUERY = "query"


def procedure(type_: ProcedureType, name: str, private: bool = False):
    pass


@overload
def query(impl: Callable) -> Callable:
    ...


def query(name: Optional[str] = None, private: Optional[bool] = None) -> "WrappedProcedure":
    def wrap_procedure(f: Callable):
        return WrappedProcedure(
            staticmethod(f),
            name=name,
            private=private,
            type_=ProcedureType.QUERY,
        )

    return wrap_procedure


def mutation(name: Optional[str] = None, private: Optional[bool] = None) -> "WrappedProcedure":
    def wrap_procedure(f: Callable):
        return WrappedProcedure(
            staticmethod(f),
            name=name,
            private=private,
            type_=ProcedureType.MUTATION,
        )

    return wrap_procedure


class Procedure:
    pass


class WrappedProcedure:
    func: Callable

    name: str
    private: bool
    type_: ProcedureType

    def __init__(
        self,
        func: Callable,
        *,
        name: str,
        private: bool,
        type_: ProcedureType,
    ):
        self.func = func
        self.name = name
        self.private = private
        self.type_ = type_
    
    def query(self, context, **params):
        if self.type_ != ProcedureType.QUERY:
            if self.private:
                raise TypeError(f"Procedure does not exist!")
            raise TypeError(f"Procedure {self.name} is not a query!")

        return self.func(context, **params)

    def mutation(self, context, **params):
        if self.type_ != ProcedureType.MUTATION:
            if self.private:
                raise TypeError(f"Procedure does not exist!")
            raise TypeError(f"Procedure {self.name} is not a mutation!")

        return self.func(context, **params)