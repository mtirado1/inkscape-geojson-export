
# Inkscape GeoJSON export

This script reads an inkscape file and converts shapes into geojson data
according to a specified projection.

The following geometries are supported:

- Polygon
- LineString / MultiLineString 
- Point

Grouped objects can be exported as a GeometryCollection.

The title tag set on Inkscape gets exported to the `name` property in the
feature's `properties` object.

## Projections

A projection object converts an (x, y) point, with positive y going down, into
a (longitude, latitude) tuple, ready to be used in a geojson object.

When creating a new projection, `toSphere()`, and `toPlane()` methods need to
be implemented to convert to spherical or cartesian coordinates, respectively.

Projections implemented:

- Mercator
- Equirectangular
- Azimuthal Equidistant

## Drawing

For polygons, the path's direction should be clockwise, and any negative
features counterclockwise.

Under Inkscape preferences --> Tools --> Node, you can toggle the option to
view a path's direction.

## Exporting

Each layer is exported as an array of GeoJSON objects. The layer name
determines the object's key.

Adding an exclamation sign `!` at the start of the layer's name will tell the
script to not export the layer.

By default, SVG paths will be exported as Polygon objects. Adding a dash (`-`)
to the layer name will tell the script to export the paths as LineString /
MultiLineString objects,

SVG Circles will get exported as GeoJSON points.

# Installation

This script requires the geojson and inkex modules in order to manipulate both
geojson data and inkscape files.

```
pip install geojson inkex
```

To install the extension, move the files inside `extension/`
to the `inkscape/extensions/` folder.

# TODO

- GeoJSON import

