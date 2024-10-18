from qgis.core import QgsApplication
from qgis.gui import QgisInterface

from .highlowpointsprovider import HighLowPointsProvider

class HighLowPointsPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.provider = HighLowPointsProvider()

    def initProcessing(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
