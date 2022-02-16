import datetime
from os import urandom
from random import randint, uniform

from faker import Faker


class FakeData:
    _faker: Faker = Faker("sv_SE")

    MIN_AGE = 18
    MAX_AGE = 72

    MIN_DATE = datetime.date(year=2020, month=1, day=1)
    MAX_DATE = datetime.datetime.today()

    @classmethod
    def configure_locale(cls, locale: str) -> None:
        cls._faker = Faker(locale=locale)

    @staticmethod
    def generate_random_int(min_: int, max_: int) -> int:
        return randint(min_, max_)

    @staticmethod
    def generate_random_float(min_: float, max_: float,
                              scale: int = 2) -> float:
        return round(uniform(min_, max_), scale)

    @classmethod
    def full_name(cls) -> str:
        return cls._faker.name()

    @classmethod
    def generate_full_names(cls, amount: int, unique: bool = True) -> list[str]:
        if unique:
            full_names_set = set()
            while len(full_names_set) < amount:
                full_names_set.add(cls._faker.name())
            return list(full_names_set)

        return [cls._faker.name() for _ in range(amount)]

    @staticmethod
    def generate_email(username: str, domain_name: str = "example", domain: str = "se") -> str:
        return f"{username}@{domain_name}.{domain}"

    @classmethod
    def generate_emails(cls, full_names: list[str], amount: int,
                        domain_name: str = "example", domain: str = "se") -> list[str]:
        emails = list()
        if amount > len(full_names):
            raise ValueError("Amount needs to be equal to or less than the length of full_names.")
        for i in range(amount):
            first_name, last_name = full_names[i].split(" ")
            email = cls.generate_email(
                username=f"{first_name.lower()}.{last_name.lower()}",
                domain_name=domain_name,
                domain=domain
            )
            emails.append(email)
        return emails

    @classmethod
    def generate_date(cls) -> datetime.date:
        return cls._faker.date_of_birth(minimum_age=cls.MIN_AGE,
                                        maximum_age=cls.MAX_AGE)

    @classmethod
    def generates_dates(cls, amount: int) -> list[datetime.date]:
        return [cls.generate_date() for _ in range(amount)]

    @classmethod
    def generate_date_time(cls, start: datetime = None, end: datetime = None) -> datetime:
        return cls._faker.date_time_between_dates(
            datetime_start=cls.MIN_DATE if not start else start,
            datetime_end=cls.MAX_DATE if not end else end)

    @classmethod
    def generate_date_times(cls, amount: int,
                            start: datetime = None, end: datetime = None) -> list[datetime]:
        return [cls.generate_date_time(start, end) for _ in range(amount)]

    @classmethod
    def text(cls, sentences: int) -> str:
        return cls._faker.paragraph(nb_sentences=sentences)

    @classmethod
    def username(cls) -> str:
        return cls._faker.user_name()

    @classmethod
    def password(cls, length: int = 12) -> str:
        return str(urandom(length))

    @classmethod
    def city(cls) -> str:
        return cls._faker.city()

    @classmethod
    def url(cls) -> str:
        return cls._faker.url()
