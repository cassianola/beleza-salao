from datetime import date, time


def minutes(value: time) -> int:
    return value.hour * 60 + value.minute


def overlap(start_a: time, duration_a: int, start_b: time, duration_b: int) -> bool:
    """Intervals [start, end); adjacent appointments do not conflict."""
    a, b = minutes(start_a), minutes(start_b)
    return a < b + duration_b and b < a + duration_a


def within_hours(start: time, duration: int, opening: time, closing: time) -> bool:
    return duration > 0 and minutes(opening) <= minutes(start) and minutes(start) + duration <= minutes(closing)


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def parse_time(value: str) -> time:
    parsed = time.fromisoformat(value)
    if parsed.second or parsed.microsecond:
        raise ValueError('Informe um horário em horas e minutos.')
    return parsed
