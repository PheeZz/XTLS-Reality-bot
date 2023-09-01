from .throttling import *


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
