from .creator import Creator
from .deleter import Deleter
from .inserter import Inserter
from .selector import Selector
from .updater import Updater


class DatabaseManager(Inserter, Selector, Updater, Deleter):
    def __init__(self):
        super().__init__()
