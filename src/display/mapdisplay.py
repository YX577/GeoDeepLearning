#!/usr/bin/python
# -*- coding: utf-8 -*-

import ee
import folium
from IPython.display import HTML

def mapdisplay(center, dicc, Tiles="OpensTreetMap",zoom_start=10):
    ''' Display a ee.Image and ee.FeatureCollection using folium
    
    Args:    
      center: Center of the map (Latitude and Longitude).
      dicc: Earth Engine Geometries or Tiles dictionary
      Tiles: Mapbox Bright,Mapbox Control Room,Stamen Terrain,Stamen Toner,stamenwatercolor,cartodbpositron.
      zoom_start: Initial zoom level for the map.
    
    Returns:
      A folium.Map object.
    '''
    center = center[::-1]
    mapViz = folium.Map(location=center,tiles=Tiles, zoom_start=zoom_start)
    for k,v in dicc.items():
      if ee.image.Image in [type(x) for x in v.values()]:
        folium.TileLayer(
            tiles = v["tile_fetcher"].url_format,
            attr  = 'Google Earth Engine',
            overlay =True,
            name  = k
          ).add_to(mapViz)
      else:
        folium.GeoJson(
        data = v,
        name = k
          ).add_to(mapViz)
    mapViz.add_child(folium.LayerControl())
    return mapViz

def embed_map(m):    
    m.save('index.html')
    with open('index.html') as f:
        html = f.read()
    iframe = '<iframe srcdoc="{srcdoc}" style="width: 100%; height: 750px; border: none"></iframe>'
    srcdoc = html.replace('"', '&quot;')
    return HTML(iframe.format(srcdoc=srcdoc))

