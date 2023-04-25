from trpc import convert_name_case


def test_simple_name_is_not_converted():
    assert convert_name_case("test") == "test"


def test_name_with_two_words_is_converted():
    assert convert_name_case("user_id") == "userId"


def test_name_with_multiple_words_is_converted():
    assert convert_name_case("get_user_by_id") == "getUserById"
