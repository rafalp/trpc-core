from inspect import signature
from typing import Any, Callable, Optional, Tuple

from .names import convert_name_case

any_type = lambda x: x

ArgTransform = Tuple[str, Callable]


def create_default_input(func: Callable) -> Optional[Tuple[ArgTransform, ...]]:
    params = signature(func).parameters

    converters = []
    for i, param_name in enumerate(params):
        if not i:
            continue

        param_type = params[param_name]
        converters.append(
            (convert_name_case(param_name), param_type.annotation or any_type)
        )

    if not converters:
        return None

    return tuple(converters)


def transform_raw_input(
    transform: Tuple[ArgTransform, ...], raw_input: Any
) -> Tuple[Any, ...]:
    normalized_input = normalize_raw_input(raw_input)

    errors = {}
    inputs = []

    for i, arg_transform in enumerate(transform):
        arg_name, arg_type = arg_transform

        try:
            arg_value = arg_type(normalized_input[i])
            inputs.append(arg_value)
        except IndexError:
            errors[arg_name] = "MISSING"

    if errors:
        raise ValueError(str(errors))

    return tuple(inputs)


def normalize_raw_input(raw_input: Any) -> Tuple[Any, ...]:
    if isinstance(raw_input, tuple):
        return raw_input

    if isinstance(raw_input, list):
        # Multiple parameters are sent as JSON lists
        # If only parameter is list, it will always be wrapped in another list
        # to avoid the ambiguity (proc([...]) -> [[...]])
        return tuple(raw_input)

    # Return tuple with single input value
    return (raw_input,)
