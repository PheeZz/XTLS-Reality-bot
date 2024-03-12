from .ip_info import IPInfo
from .localizer import Localizer
from .mailer import Mailer

localizer = Localizer()

__all__ = ["localizer", "IPInfo"]
