from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,
    QgsProcessingFeedback,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterFileDestination,
    QgsProviderRegistry,
    QgsVectorLayer,
    QgsField,
    QgsFields,
    QgsFeature,
    QgsWkbTypes,
)

from qgis.PyQt.QtCore import QVariant

class HighLowPoints(QgsProcessingAlgorithm):
    LINES = 'LINES'
    RASTER = 'RASTER'
    STEP = 'STEP'
    VERT = 'VERT'
    OUTPUT = 'OUTPUT'

    def name(self):
        return "highlowpoints"

    def displayName(self):
        return "High/Low Points Along Lines"

    def createInstance(self):
        return HighLowPoints()

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.LINES,
                'Lines Layer',
                [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.RASTER,
                'DEM',
                [QgsProcessing.TypeRaster]
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP,
                'Sampling Step Distance',
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Output',
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        self.out_fields = QgsFields()
        self.out_fields.append(QgsField("feature", QVariant.Int))
        self.out_fields.append(QgsField("dist", QVariant.Double))
        self.out_fields.append(QgsField("type", QVariant.String))
        self.out_fields.append(QgsField("elev", QVariant.Double))
        self.out_fields.append(QgsField("tlen", QVariant.Double))

        self.source = self.parameterAsSource(
            parameters,
            self.LINES,
            context
        )
        self.dem = self.parameterAsRasterLayer(
            parameters,
            self.RASTER,
            context
        )
        self.step = self.parameterAsDouble(
            parameters,
            self.STEP,
            context
        )
        self.sink = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            self.out_fields,
            QgsWkbTypes.Point,
            self.source.sourceCrs()
        )
        self.dest_id = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            self.out_fields,
            QgsWkbTypes.Point,
            self.source.sourceCrs()
        )
        self.dem_provider = self.dem.dataProvider()
        self.pt_list = []
        self.len_list = []
        self.hp_list = []
        self.lp_list = []

        self.getSamples()

        for hp in self.hp_list:
            self.sink.addFeature(hp, QgsFeatureSink.FastInsert)
        for lp in self.lp_list:
            self.sink.addFeature(lp, QgsFeatureSink.FastInsert)

        return {self.OUTPUT: self.dest_id}

    def getSamples(self):
        feat_count = 0

        for ln_feat in self.source.getFeatures():
            geom = ln_feat.geometry()
            num_vertices = len(geom.asPolyline())
            accum = self.step
            step_count = 1
            tlen = geom.length()
            self.len_list.append(tlen)
            pt_feature = QgsFeature(outFields)
            pt_feature.setGeometry(geom.vertexAt(0))
            pt_feature['feature'] = feat_count
            pt_feature['dist'] = 0.00
            pt_feature['elev'], success = self.dem_provider.sample(pt_feature.geometry().asPoint(), 1)
            pt_feature['tlen'] = tlen
            self.pt_list.append(pt_feature)

            while accum < tlen:
                new_pt_feature = geom.interpolate(step_count * self.step)
                pt_feature = QgsFeature(self.out_fields)
                pt_feature.setGeometry(new_pt_feature)
                pt_feature['feature'] = feat_count
                pt_feature['dist'] = step_count * self.step
                pt_feature['elev'], success = self.dem_provider.sample(pt_feature.geometry().asPoint(), 1)
                pt_feature['tlen'] = tlen
                self.pt_list.append(pt_feature)
                accum += step
                step_count += 1
            pt_feature.setGeometry(geom.vertexAt(num_vertices - 1))
            pt_feature['feature'] = feat_count
            pt_feature['dist'] = tlen
            pt_feature['elev'], success = self.dem_provider.sample(pt_feature.geometry().asPoint(), 1)
            pt_feature['tlen'] = tlen
            pt_list.append(pt_feature)
            feat_count += 1
