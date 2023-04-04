
function getRadiusofEarth(lat_radian) {
    // Get radius of earth at given latitude km
  
    var r1 = 6378.137; // radius at equator
    var r2 = 6356.752; // radius at poles
    var a = r1 * Math.cos(lat_radian);
    var b = r2 * Math.sin(lat_radian);
    var num = Math.pow((a * r1), 2) + Math.pow((b * r2), 2);
    var den = Math.pow(a, 2) + Math.pow(b, 2);
    
    return Math.sqrt(num / den); // radius of earth at given latitude in km
  }
  
  
  function changeInLongitude(resolution, latitude) {
      // - resolution in metres, latitude in degrees
      // - moving on same latitude, (change in longitude)
    
      var lat_rad = (Math.PI / 180) * latitude; // convert to radian
      var r_earth = getRadiusofEarth(lat_rad); // radius of earth at given latitude
      var r_ring = r_earth * (Math.cos(lat_rad)) * 1000; //radius of ring at given latitude in meters
    
      return (resolution * 360) / (2 * r_ring * Math.PI);
      }
    
    function changeInLatitude(resolution, latitude) {
      // - resolution in metres, latitude in degrees
      // - moving on same longitude, (change in latitude)
    
      var lat_rad = (Math.PI / 180) * latitude; // convert to radian
      var r_earth = getRadiusofEarth(lat_rad); // radius of earth at given latitude
      // r_earth = 6371.001; // average radius of earth (in km)
      r_earth *= 1000; // in metres
    
      return (resolution * 360) / (2 * r_earth * Math.PI);
    }
    
    function genMatrix(lon1, lat1, lon2, lat2, res) {
        // generate matrix of coordinates using corner points
        var result = [];
        var lat_diff = Math.abs(changeInLatitude(res, lat1));
        var lon_diff = Math.abs(changeInLongitude(res, lat1));
      
        var start_lat = Math.max(lat1, lat2);
        var start_lon = Math.min(lon1, lon2);
        var end_lat = Math.min(lat1, lat2);
        var end_lon = Math.max(lon1, lon2);
      
        lat1 = start_lat;
        lon1 = start_lon;
        lat2 = end_lat;
        lon2 = end_lon;
      
        print("start: ", start_lat, start_lon);
        print("end: ", end_lat, end_lon);
      
        while (start_lat > end_lat) {
          var row = [];
          var temp_lon = start_lon;
          while (temp_lon <= end_lon) {
            row.push([start_lat, temp_lon]);
            temp_lon += lon_diff;
          }
          start_lat -= lat_diff;
          result.push(row);
        }
      
        print("shape: ", result.length, result[0].length);
        return result;
      }
  
  // Define a function to get elevation for a given point
  function getElevationHelper(point) {
      var elevation = ee.Image('USGS/SRTMGL1_003').reduceRegion({
        reducer: ee.Reducer.mean(),
        geometry: ee.Geometry.Point(point),
        scale: 30
      }).get('elevation');
      return elevation;
  }
  
  function genElevationMatrix(lon1, lat1, lon2, lat2, res) {
      var bounding_box = genMatrix(lon1, lat1, lon2, lat2, res);
      print("Bounding Box: ", bounding_box);
  
      // Map the function over all the points to get a list of elevations
      var elevations = points.map(function(point) {
        return [getElevationHelper(point[0]), getElevationHelper(point[1])];
      });
  
      return elevations;
  }
  
  var res = 50;
  var elevations = genElevationMatrix(77.0845, 32.3166, 77.2342, 32.1795, res);
  print(elevations);
  
  


  // new code

  var dataset = ee.Image('CGIAR/SRTM90_V4');
// var elevation = dataset.select('elevation');
// var slope = ee.Terrain.slope(elevation);
// Map.setCenter(77.17245991760569,32.2446176598011, 10);
// Map.addLayer(slope, {min: 0, max: 60}, 'slope');

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





// Load the SRTM dataset
var elevation = ee.Image('USGS/SRTMGL1_003');

// Define the matrix of coordinate points as a 2D list
var points = [
  [77.10104878479319,32.346191952341016], [77.38669331604319,32.27771435514376],
  [77.12302144104319,32.123159941913215], [77.30704243713694,32.10803904148201],
  [77.06946309143382,32.23358274667811]
];

// Convert the matrix of coordinate points to a feature collection
var featureCollection = ee.FeatureCollection(
  ee.List(points).map(function(point) {
    return ee.Feature(ee.Geometry.Point(point));
  })
);

// Sample the elevation values at each point in the feature collection
var elevationValues = elevation.sampleRegions({
  collection: featureCollection,
  scale: 30, // the resolution of the SRTM dataset is 30 meters
  tileScale: 16 // increase this value to improve performance
});

// Convert the elevation values to a 2D list
var elevationList = elevationValues.aggregate_array('elevation');
var elevationArray = ee.Array.cat([elevationList], 1);
var elevationMatrix = elevationArray.toList().map(function(row) {
  return ee.List(row);
});

// Print the elevation matrix to the console
print(elevationMatrix);



