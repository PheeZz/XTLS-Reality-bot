from loguru import logger
from .connector import DatabaseConnector


class Updater(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Updater object was initialized")

    async def add_days_to_user_subscription(self, user_id: int, days: int) -> bool:
        """
        Add days to user subscription if subscription_end_date >= current_date
        else set subscription_end_date to current_date + days
        """
        query = f"""--sql
            UPDATE users
            SET subscription_end_date = CASE
                WHEN subscription_end_date >= CURRENT_DATE
                THEN subscription_end_date + INTERVAL '{days} days'
                ELSE CURRENT_DATE + INTERVAL '{days} days'
            END
            WHERE user_id = {user_id};
        """
        if await self._execute_query(query) is False:
            logger.error(
                f"Error while adding {days} days to user {user_id} subscription"
            )
            return False
        logger.debug(f"Added {days} days to user {user_id} subscription")
        return True
