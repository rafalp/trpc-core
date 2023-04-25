from enum import Enum
from typing import Any, Callable, Optional, overload

from .inputs import create_default_input, transform_raw_input
from .names import convert_name_case


class ProcedureType(str, Enum):
    MUTATION = "mutation"
    QUERY = "query"


def procedure(type_: ProcedureType, name: str, private: bool = False):
    pass


@overload
def query(impl: Callable) -> Callable:
    ...


def query(
    name: Optional[str] = None,
    input: Optional[Callable] = None,
    private: Optional[bool] = None,
) -> "WrappedProcedure":
    def wrap_procedure(func: Callable) -> "WrappedProcedure":
        return create_wrapped_procedure(
            func,
            ProcedureType.QUERY,
            name=name,
            input=input,
            private=private,
        )

    return wrap_procedure


@overload
def mutation(impl: Callable) -> Callable:
    ...


def mutation(
    name: Optional[str] = None,
    input: Optional[Callable] = None,
    private: Optional[bool] = None,
) -> "WrappedProcedure":
    def wrap_procedure(func: Callable) -> "WrappedProcedure":
        return create_wrapped_procedure(
            func,
            ProcedureType.MUTATION,
            name=name,
            input=input,
            private=private,
        )

    return wrap_procedure


class Procedure:
    pass


def create_wrapped_procedure(
    func: Callable,
    type_: ProcedureType.MUTATION,
    name: Optional[str] = None,
    input: Optional[Callable] = None,
    private: Optional[bool] = None,
) -> "WrappedProcedure":
    if input:
        input_type = input
    else:
        input_type = create_default_input(func)

    return WrappedProcedure(
        func,
        name=name or convert_name_case(func.__name__),
        private=private or False,
        type_=type_,
        input_type=input_type,
    )


class WrappedProcedure:
    func: Callable
    input_type: Optional[Callable]

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
        input_type: Callable,
    ):
        self.func = func
        self.input_type = input_type

        self.name = name
        self.private = private
        self.type_ = type_

    def query(self, context: Any, raw_input: Any):
        return self.execute(ProcedureType.QUERY, context, raw_input)

    def mutation(self, context: Any, raw_input: Any):
        return self.execute(ProcedureType.MUTATION, context, raw_input)

    def execute(self, type_: ProcedureType, context: Any, raw_input: Any) -> Any:
        if self.type_ != type_:
            if self.private:
                raise TypeError("Procedure does not exist!")
            raise TypeError(f"Procedure {self.name} is not a {str(type_).lower()}!")

        if self.input_type:
            proc_args = transform_raw_input(self.input_type, raw_input)
            return self.func(context, *proc_args)

        return self.func(context)
