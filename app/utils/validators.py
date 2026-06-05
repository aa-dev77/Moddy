import re

URL_PATTERN = re.compile(
    r"(https?:\/\/|t\.me\/|www\.)",
    re.IGNORECASE
)

USERNAME_PATTERN = re.compile(
    r"@\w+",
    re.IGNORECASE
)


def contains_advertisement(text: str) -> bool:
    if not text:
        return False

    if URL_PATTERN.search(text):
        return True

    if USERNAME_PATTERN.search(text):
        return True

    return False