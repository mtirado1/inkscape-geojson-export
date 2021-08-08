#!/usr/bin/python3

import inkex
import geojson
import projection
 
class GeoExport:
    def __init__(self):
        self.exportObject = {}
   
    def dump(self):
        return geojson.dumps(self.exportObject)
   
    def getLayers(self, document):
        layers = document.xpath('//svg:g[@inkscape:groupmode="layer"]', namespaces=inkex.NSS)
        return map(lambda layer: (layer, layer.get("inkscape:label")), layers)
   
    def getTitle(self, node):
        title= node.find(inkex.addNS('title', 'svg'))
        if title is not None:
            return title.text
        return None
   
    def getProjectedPaths(self, node):
        node.apply_transform()
        d = node.get('d')
        return list(map(lambda subpath:
            list(map(lambda csp: self.projection.toSphere(csp[1][0], csp[1][1]), subpath)),
            inkex.paths.CubicSuperPath(d)
        ))
   
    def parseObject(self, node, isLineLayer):
        if node.tag == inkex.addNS('g', 'svg'): # Feature Collection
            features = []
            for child in node:
                if child.tag != inkex.addNS('g', 'svg'): # Avoid nested groups
                    obj = self.parseObject(child, isLineLayer)
                    if obj is not None:
                        features.append(obj)
            return geojson.GeometryCollection(features,
                properties = {'name': self.getTitle(node)}
            )
        elif node.tag == inkex.addNS('path', 'svg'): # Polygon / Line
            paths = self.getProjectedPaths(node)
            if isLineLayer:
                if len(paths) == 1:
                    return geojson.LineString(paths[0],
                        properties = {'name': self.getTitle(node)}
                    )
                else:
                    return geojson.MultiLineString(paths,
                        properties = {'name': self.getTitle(node)}
                    )
            else:
                return geojson.Polygon(paths,
                    properties = {'name': self.getTitle(node)}
                )
        elif node.tag == inkex.addNS('circle', 'svg'): # Point
            x = float(node.get("cx"))
            y = float(node.get("cy"))
            return geojson.Point(self.projection.toSphere(x, y),
                properties = {
                    'name': self.getTitle(node),
                    'type': node.get("inkscape:label")
                }
            )
        return None
 
    def processFile(self, fileName, projection):
        document = inkex.elements.load_svg(fileName)
        return self.processDocument(document, projection)
  
    def processDocument(self, document, projection):
        svg = document.getroot()
        width = float(svg.get('viewBox').split(' ')[2])
        height = float(svg.get('viewBox').split(' ')[3])
        self.projection = projection.dimensions(width, height)
  
        for layer, className in self.getLayers(document):
            isLineLayer = False
            if className[0] == '!':
                continue
            if className[0] == '-':
                isLineLayer = True
                className = className[1:]
           
            if className not in self.exportObject:
                self.exportObject[className] = []
           
            for node in layer:
                geo = self.parseObject(node, isLineLayer)
                self.exportObject[className].append(geo)
  
        return self.exportObject
 
 
# exporter = GeoExport()
# exporter.processFile('map1.svg', projection.Mercator())
# exporter.processFile('map2.svg', projection.AzimuthalEquidistant().center(90, 180))
# print(exporter.dump())
