from enum import Enum


class SubscriptionStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    pending = 'pending'
    blocked = 'blocked'
