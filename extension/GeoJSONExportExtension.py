import inkex
from exportgeojson import *
from projection import projectionList


class GeoExportExtension(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument('--projection',
            type=str,
            dest='projection', default='Equirectangular',
            help='Projection')
        self.arg_parser.add_argument("--latitude",
            type=float,
            dest='latitude', default=0,
            help='Center latitude')
        self.arg_parser.add_argument("--longitude",
            type=float,
            dest='longitude', default=0,
            help='Center longitude')
        self.arg_parser.add_argument('--outputfile',
            type=str,
            dest='outputFile', default='',
            help='Output file')
        self.arg_parser.add_argument('--overwrite',
            type=inkex.Boolean,
            dest='overwrite', default='True',
            help='Overwrite file')

    def effect(self):
        document = self.document
        exporter = GeoExport()
        
        latitude = self.options.latitude
        longitude = self.options.longitude
        projection = projectionList[self.options.projection]().center(latitude, longitude)
        # Load if not overwriting
        if not self.options.overwrite:
            with open(self.options.outputFile, 'r') as jsonData:
                data = jsonData.read()
                exporter.exportObject = json.loads(data)

        exporter.processDocument(document, projection)

        jsonFile = open(self.options.outputFile, 'w')
        jsonFile.write(exporter.dump())
        jsonFile.close()

if __name__ == '__main__':
    e = GeoExportExtension()
    e.run()
