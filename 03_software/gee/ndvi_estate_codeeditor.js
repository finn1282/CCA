// SawitSense M5 — paste into https://code.earthengine.google.com (visual check / Drive export).
// Same method as gee/ndvi_estate.py. Attribution: "Contains modified Copernicus Sentinel data <year>".
var lon = 103.30, lat = 1.96, sizeKm = 4, csThreshold = 0.60;
var half = sizeKm / 2 / 111.32;
var aoi = ee.Geometry.Rectangle([lon - half, lat - half, lon + half, lat + half]);
var palm = ee.ImageCollection('BIOPAMA/GlobalOilPalm/v1').select('classification').mosaic().lte(2);
var csp = ee.ImageCollection('GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED');
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED').filterBounds(aoi)
  .linkCollection(csp, ['cs'])
  .map(function (img) {
    return img.normalizedDifference(['B8', 'B4']).rename('ndvi')
      .updateMask(img.select('cs').gte(csThreshold)).updateMask(palm);
  });
var end = ee.Date(Date.now()).update(null, null, 1);
var months = ee.List.sequence(1, 24).map(function (i) { return end.advance(ee.Number(i).multiply(-1), 'month'); });
var monthly = ee.ImageCollection(months.map(function (d) {
  d = ee.Date(d);
  var c = s2.filterDate(d, d.advance(1, 'month'));
  return c.median().set('system:time_start', d.millis()).set('n', c.size());
})).filter(ee.Filter.gt('n', 0));
var latest = monthly.sort('system:time_start', false).first();
var hist = monthly.sort('system:time_start', false).toList(30).slice(1);
hist = ee.ImageCollection(hist);
var z = latest.subtract(hist.mean()).divide(hist.reduce(ee.Reducer.stdDev()));
Map.centerObject(aoi, 14);
Map.addLayer(latest.clip(aoi), {min: 0.5, max: 0.9, palette: ['brown', 'yellow', 'green']}, 'NDVI latest month');
Map.addLayer(z.clip(aoi), {min: -2.5, max: 2.5, palette: ['b2182b', 'ef8a62', 'f7f7f7', '67a9cf', '2166ac']}, 'NDVI z-score');
print(ui.Chart.image.series(monthly, aoi, ee.Reducer.median(), 10).setOptions({title: 'Estate median NDVI'}));
Export.image.toDrive({image: latest.toFloat(), description: 'sawitsense_ndvi_latest', folder: 'sawitsense',
  region: aoi, scale: 10, fileFormat: 'GeoTIFF'});
