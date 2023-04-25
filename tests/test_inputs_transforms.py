from trpc import create_default_input, transform_raw_input


def test_default_input_transform_for_callable_with_context_only_is_none():
    def my_proc(context):
        ...

    transform = create_default_input(my_proc)
    assert transform is None


def test_default_input_transform_for_callable_with_single_arg_is_tuple():
    def my_proc(context, name: str):
        ...

    transform = create_default_input(my_proc)
    assert transform == (str,)


def test_default_input_transform_for_callable_with_multiple_args_is_tuple():
    def my_proc(context, a: int, b: int):
        ...

    transform = create_default_input(my_proc)
    assert transform == (int, int)


def test_default_input_transform_can_be_used_to_transform_multiple_inputs():
    def my_proc(context, a: int, b: int):
        ...

    transform = create_default_input(my_proc)
    result = transform_raw_input(transform, ["2", "4"])
    assert result == (2, 4)
