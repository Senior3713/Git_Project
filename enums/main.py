from enum import Enum


class LangEnum(Enum):
    UZ = "uz"
    EN = "en"


class VolEnum(Enum):
    SOFT = "soft"
    HARD = "hard"


class MoneyTypeEnum(Enum):
    DOLLAR = "$"
    UZS = "sum"


class StatusEnum(Enum):
    PENDING = "pending"
    APPROVED = "approved"
