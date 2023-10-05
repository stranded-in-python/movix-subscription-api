from enum import Enum


class Currency(str, Enum):
    rub = 'RUB'


class PaymentStatus(str, Enum):
    open = "open"
    paid = "paid"
    overdue = "overdue"
    canceled = 'canceled'
    refunded = 'refunded'


class SubscriptionStatus(str, Enum):
    active = 'active'
    inactive = 'inactive'
    pending = 'pending'
    blocked = 'blocked'
