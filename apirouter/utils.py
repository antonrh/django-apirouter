def removeprefix(string: str, *, prefix: str):
    if string.startswith(prefix):
        start = len(prefix)
        return string[start:]
    return string
