# DON'T TOUCH THIS IMPORT
from aiogram import Dispatcher

from loader import dp

from .admin import register_admin_handlers
from .user import register_user_handlers


def setup(dp: Dispatcher):
    register_user_handlers(dp)
    register_admin_handlers(dp)
