from enum import Enum

class UserType(Enum):
    PROPERTY_INVESTOR = 1
    HOME_BUYER = 2
    IRRELEVANT = 3


class ObjectiveCategory(Enum):
    INVESTMENT_OBJECTIVE = 1
    IRRELEVANT = 2

