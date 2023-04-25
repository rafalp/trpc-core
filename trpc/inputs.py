from inspect import signature
from typing import Any, Callable, Optional, Tuple

any_type = lambda x: x


def create_default_input(func: Callable) -> Optional[Tuple[Callable, ...]]:
    params = signature(func).parameters

    converters = []
    for i, param_name in enumerate(params):
        if not i:
            continue

        param_type = params[param_name]
        converters.append(param_type.annotation or any_type)

    if not converters:
        return None

    return tuple(converters)


def transform_raw_input(
    transform: Tuple[Callable, ...], raw_input: Any
) -> Tuple[Any, ...]:
    normalized_input = normalize_raw_input(raw_input)

    return tuple(
        transform_func(normalized_input[i])
        for i, transform_func in enumerate(transform[: len(normalized_input)])
    )


def normalize_raw_input(raw_input: Any) -> Tuple[Any, ...]:
    if isinstance(raw_input, tuple):
        return raw_input

    if isinstance(raw_input, list):
        # Multiple parameters are sent as JSON lists
        # If only parameter is list, it will always be wrapped in another list
        # to avoid the ambiguity (proc([...]) -> [[...]])
        return tuple(raw_input)

    # Return tuple with only input
    return (raw_input,)
