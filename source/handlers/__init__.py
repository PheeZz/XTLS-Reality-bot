# DON'T TOUCH THIS IMPORT
from loader import dp
from aiogram import Dispatcher

from .user import register_user_handlers
from .admin import register_admin_handlers


def setup(dp: Dispatcher):
    register_user_handlers(dp)
    register_admin_handlers(dp)
