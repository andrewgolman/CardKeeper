from enum import Enum


class _SearchableEnum(Enum):
    @classmethod
    def has(cls, value):
        for k, v in cls.__members__.items():
            if v.value == value:
                return v
        return None

    @classmethod
    def values(cls):
        ans = []
        for k, v in cls.__members__.items():
            ans.append(str(v.value))
        return ans


class GenGoalType(_SearchableEnum):
    SCIENCE = 'Science'
    SPEECH = 'Speech'
    BELLETRISTIC = 'Belletristic'


class NotificationType(_SearchableEnum):
    TWICE_A_DAY = 'Twice a day'
    DAILY = 'Daily'
    WEEKLY = 'Weekly'
    NEVER = 'Never'


class PrivacyType(_SearchableEnum):
    PRIVATE = 'private'
    PROTECTED = 'protected'
    PUBLIC = 'public'


class CardStatusType(_SearchableEnum):
    ACTIVE = 'Active'
    RESERVED = 'Reserved'
    NOT_READY = 'Not ready'
    DEPRECATED = 'Deprecated'
    LEARNED = 'Learned'


class RightsType(_SearchableEnum):
    ADMIN = 'admin'
    USER = 'user'
    INVITED = 'invited'
    APPLIED = 'applied'


class InvitationType(_SearchableEnum):
    FROM_GROUP = 'from a group'
    FROM_USER = 'from a user'


class CardType(_SearchableEnum):
    SHORT = 'Short'
    CONSTRUCTION = 'Construction'
    SENTENCE = 'Sentence'
