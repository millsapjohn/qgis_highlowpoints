from .plugin import HighLowPointsPlugin

def classFactory(iface):
    return HighLowPointsPlugin(iface)
