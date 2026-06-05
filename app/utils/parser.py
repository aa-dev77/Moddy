import re

TIME_PATTERN = re.compile(r"^(\d+)([mh])$")


def parse_duration(value: str) -> int | None:
    match = TIME_PATTERN.match(value.lower())

    if not match:
        return None

    amount = int(match.group(1))
    unit = match.group(2)

    if unit == "m":
        return amount * 60

    if unit == "h":
        return amount * 3600

    return None