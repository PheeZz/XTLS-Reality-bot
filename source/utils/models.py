from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int
    username: str
    is_not_banned: str
    is_active_subscription: bool
    subscription_end_date: datetime
    configs_count: int
    bonus_configs_count: int
    unused_configs_count: int
    created_at: datetime
