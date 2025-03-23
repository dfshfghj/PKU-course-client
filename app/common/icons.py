from enum import Enum
from qfluentwidgets import getIconColor, Theme, FluentIconBase
from .. import resources_rc

class LocalIcon(FluentIconBase, Enum):
    """Local icons"""

    PKUFULL = 'PKUFull'
    PKU = 'PKU'

    def path(self, theme=Theme.AUTO):
        return f':/images/icons/{self.value}_{getIconColor(theme)}.svg'