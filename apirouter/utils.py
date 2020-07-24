def removeprefix(string: str, *, prefix: str):
    if string.startswith(prefix):
        start = len(prefix)
        return string[start:]
    return string


def compose_decorators(*decorators):
    def decorator(func):
        for dec in reversed(decorators):
            func = dec(func)
        return func

    return decorator
