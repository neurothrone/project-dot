from datetime import datetime


class Day:
    @staticmethod
    def part_of_day(datetime_: datetime) -> str:
        hour = datetime_.hour
        if 5 < hour < 12:
            return "Morning"
        elif 12 <= hour < 17:
            return "Afternoon"
        elif 17 <= hour < 21:
            return "Evening"
        else:
            return "Night"


def time_of_day_message(datetime_: datetime) -> str:
    return f"Good {Day.part_of_day(datetime_)}"


def datetime_format(datetime_: datetime) -> str:
    return datetime_.strftime("%Y-%m-%d %H:%M:%S")


def date_format(datetime_: datetime) -> str:
    return datetime_.strftime("%Y-%m-%d")


def time_format(datetime_: datetime) -> str:
    return datetime_.strftime("%H:%M:%S")


def time_difference_to_now(_datetime: datetime) -> str:
    now = datetime.utcnow()
    difference = now - _datetime
    return str(difference.seconds // 60)
