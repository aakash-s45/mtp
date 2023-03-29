var dataset = ee.Image('CGIAR/SRTM90_V4');
var elevation = dataset.select('elevation');
var slope = ee.Terrain.slope(elevation);
Map.setCenter(77.14350652883557,32.33810603871073, 10);
Map.addLayer(slope, {min: 0, max: 60}, 'slope');


// Create a MultiPoint object
var multiPoint = geometry;

// Flatten the coordinates of the MultiPoint object
var flattenedCoords = multiPoint.coordinates().flatten();

// Loop through the flattened coordinates and extract the latitude and longitude values
for (var i = 0; i < flattenedCoords.length().getInfo(); i += 2) {
  var lat = ee.Number(flattenedCoords.get(i + 1));
  var lon = ee.Number(flattenedCoords.get(i));
  print('Point ' + i/2 + ': Latitude=' + lat.getInfo() + ', Longitude=' + lon.getInfo());
}


// Create a LineString object with a specified path
var path = ee.Geometry.LineString(
  [[77.12579025300657,32.478462710303546], [77.18072189363157,32.65438217320367], [77.00768722566282,32.580352871899244]]
);

// Define a visualization style for the path
var pathStyle = {
  color: 'blue',
  width: 2
};

// Add the path to the map
Map.addLayer(path, pathStyle, 'Path');

var dataset = ee.Image('CGIAR/SRTM90_V4');
var elevation = dataset.select('elevation');
var slope = ee.Terrain.slope(elevation);
Map.setCenter(-112.8598, 36.2841, 10);
Map.addLayer(slope, {min: 0, max: 60}, 'slope');
