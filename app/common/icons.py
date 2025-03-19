from enum import Enum
from qfluentwidgets import getIconColor, Theme, FluentIconBase


class LocalIcon(FluentIconBase, Enum):
    """Local icons"""

    PKUFULL = 'PKUFull'
    PKU = 'PKU'

    def path(self, theme=Theme.AUTO):
        return f'app/images/icons/{self.value}_{getIconColor(theme)}.svg'