from .inserter import Inserter
from .selector import Selector
from .updater import Updater
from .deleter import Deleter


class DatabaseManager(Inserter, Selector, Updater, Deleter):
    def __init__(self):
        super().__init__()
