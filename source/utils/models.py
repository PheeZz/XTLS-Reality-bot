from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class UserInfo:
    user_id: int
    username: str
    is_not_banned: str
    is_active_subscription: bool
    subscription_end_date: datetime
    configs_count: int
    bonus_configs_count: int
    unused_configs_count: int
    created_at: datetime


@dataclass
class VpnConfigDB:
    config_id: int
    user_id: int
    config_name: str
    config_uuid: str


class SubscriptionStatus(Enum):
    expired = "EXPIRED"
    last_day_left = "LAST_DAY_LEFT"
    two_days_left = "TWO_DAYS_LEFT"


@dataclass
class GlobalStatistics:
    users_registered: int
    users_banned: int
    users_with_active_subscription: int
    users_with_expired_subscription: int
    users_with_last_day_left_subscription: int
    users_with_two_days_left_subscription: int
    active_configs_count: int
