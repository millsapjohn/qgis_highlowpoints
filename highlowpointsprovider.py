from qgis.core import QgsProcessingProvider

from .highlowpointstool import HighLowPoints

class HighLowPointsProvider(QgsProcessingProvider):
    def load(self):
        self.refreshAlgorithms()

        return True

    def loadAlgorithms(self):
        self.addAlgorithm(HighLowPoints())

    def id(self):
        return "highlowpoints"

    def name(self):
        return "High/Low Points Along Lines"

    def longName(self):
        return self.name()
