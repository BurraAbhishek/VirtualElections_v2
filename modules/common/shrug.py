from curses.ascii import isalnum


def is_shrug(s: str) -> bool:
    result = True
    for c in s:
        if not isalnum(c):
            result = False
    return result
