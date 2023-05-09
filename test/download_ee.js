var dataset = ee.Image('USGS/SRTMGL1_003');
var elevation = dataset.select('elevation');
var slope = ee.Terrain.slope(elevation);
Map.setCenter(79.36002854900923,30.392200245005014, 6);
Map.addLayer(slope, {min: 0, max: 60}, 'slope');


var rec = ee.Geometry.Rectangle(69.33658656724417,36.964887510231584,85.06900844224417,9.857469011202983); 
print(rec, 'rec'); 
Map.addLayer(rec, {color: 'red'})

var bbox = ee.Geometry.BBox(69.33658656724417,36.964887510231584,85.06900844224417,9.857469011202983);
print(bbox, 'bbox'); 
Map.addLayer(bbox, {color: 'green'})

Export.image.toDrive({
  image: dataset,
  description: 'india',
  region: bbox,
  fileFormat: 'GeoTIFF',
  formatOptions: {
    cloudOptimized: false
  },
  maxPixels: 1e12
});