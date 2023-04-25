def convert_name_case(name: str) -> str:
    """Converts str with name from snake_case to pascalCase.

    Uses simple conversion logic where underscore characters are stripped and
    every character preceded by an underscore is made upper case:

    - 'test' -> 'test'
    - 'test2' -> 'test2'
    - 'test_name' -> 'testName'
    - 'lorem_ipsum_dolor' -> 'loremIpsumDolor'
    """
    if "_" not in name:
        return name

    fin_name = ""

    for i, c in enumerate(name):
        if c == "_":
            continue
        if i:
            if name[i - 1] == "_":
                fin_name += c.upper()
            else:
                fin_name += c
        else:
            fin_name += c

    return fin_name
