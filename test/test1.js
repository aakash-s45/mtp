var dataset = ee.Image('CGIAR/SRTM90_V4');
var elevation = dataset.select('elevation');
var slope = ee.Terrain.slope(elevation);
Map.setCenter(77.17245991760569,32.2446176598011, 10);
Map.addLayer(slope, {min: 0, max: 60}, 'slope');

// 1,2 ->bbox 3,4 -> src,des 5->center

// var multiPoint = geometry;

// function extractCoordinates(multiPoint) {
//   // Flatten the coordinates of the MultiPoint object
//   var flattenedCoords = multiPoint.coordinates().flatten();
//   var coordinates = [];
  
//   // Loop through the flattened coordinates and extract the latitude and longitude values
//   for (var i = 0; i < flattenedCoords.length().getInfo(); i += 2) {
//     var lat = ee.Number(flattenedCoords.get(i + 1));
//     var lon = ee.Number(flattenedCoords.get(i));
//     coordinates.push([lon.getInfo(), lat.getInfo()]);
//   }

//   // Return the list of coordinates
//   return coordinates;
// }

// // 0,1 -> bbox 
// // 2,3 -> src,des 
// //   4 -> center
// var map_p = extractCoordinates(multiPoint);
// Map.setCenter(map_p[4][0], map_p[4][1], 10);
// // var bbox = ee.Geometry.Rectangle(map_p[0][0],map_p[0][1],map_p[1][0],map_p[1][1]);
// var bbox = ee.Geometry.BBox(map_p[0][0], map_p[0][1], map_p[1][0], map_p[1][1]);

// // Clip the SRTM dataset to the bounding box
// // Define the resolution of the sample data

// var srtm_clipped = dataset.clip(bbox);
// print(typeof(srtm_clipped))
// var resolution = 50; // meters
// // Sample the SRTM dataset at the given resolution
// var elevation = srtm_clipped.sample({
//   region: bbox,
//   scale: resolution,
//   numPixels: 1000
// });

// // Extract the elevation values from the feature collection
// var elevation_values = elevation.aggregate_array('elevation');

// // Convert the elevation values to a JavaScript array
// elevation_values.evaluate(function(values) {
//   // Define the size of the matrix
//   var rows = bbox.bounds().getInfo().coordinates[0].length - 1;
//   var cols = rows;
  
//   // Compute the minimum and maximum elevation values
//   var minValue = Math.min.apply(null, values);
//   var maxValue = Math.max.apply(null, values);
//   print('Minimum elevation: ' + minValue);
//   print('Maximum elevation: ' + maxValue);

//   // Convert the array to a 2D array
//   var matrix = Array.from(values).reduce(function(result, value, index) {
//     var row = Math.floor(index / cols);
//     var col = index % cols;
//     if (!result[row]) {
//       result[row] = [];
//     }
//     result[row][col] = value;
//     return result;
//   }, []);

//   // Print the matrix
//   print(matrix);


//   // Add the bounding box to the map
//   Map.addLayer(bbox, {}, 'Bounding Box');

//   // Add the SRTM dataset to the map
//   Map.addLayer(srtm_clipped, {min:minValue, max:maxValue}, 'SRTM');

//   // Add a color ramp to the map
//   var colors = ['blue', 'green', 'yellow', 'red'];
//   var visParams = {min: minValue, max: maxValue, palette: colors};
//   Map.addLayer(srtm_clipped, visParams, 'SRTM_1');
// });














// // Create a LineString object with a specified path
// var path = ee.Geometry.LineString(
//   [[77.12579025300657,32.478462710303546], [77.18072189363157,32.65438217320367], [77.00768722566282,32.580352871899244]]
// );

// // Define a visualization style for the path
// var pathStyle = {
//   color: 'blue',
//   width: 2
// };

