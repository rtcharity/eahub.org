import MarkerClusterer from '@google/markerclusterer';

import Heatmap from './heatmap';
import LocationCluster from './locationCluster';
import LocationClusters from './locationClusters';
import Marker from './marker';
import Profile from './profile';

window.initHeatmapFull = function initHeatmapFull(queryStringMap) {
  var mapParams = getMapParams();
  var mapLocations = JSON.parse(document.getElementById('map-locations').textContent);
  var newMap = new Heatmap(queryStringMap, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, window.isIE)
  newMap.setup();
}

window.initHeatmapList = function initHeatmapList(queryStringMap) {
  var mapParams = getMapParams();
  var mapLocations = JSON.parse(document.getElementById('map-locations').textContent);
  var newMap = new Heatmap(queryStringMap, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, window.isIE);
  newMap.render(mapLocations.profiles, mapLocations.private_profiles);
}

window.initHeatmapProfile = function initHeatmapProfile(mapLocations, htmlElements) {
  console.log("OY")
  var mapParams = getMapParams();
  mapParams.htmlElements = htmlElements;
  var newMap = new Heatmap(undefined, mapLocations, mapParams.mapModules, mapParams.externalModules, mapParams.htmlElements, window.isIE);
  newMap.renderProfilePageMap();
}

function getMapParams() {
  var mapSelectorInd = document.getElementById('map_selector_ind');
  var mapSelectorGroups = document.getElementById('map_selector_groups');
  var mapElement = document.getElementById('map')
  var htmlElements = {
    selectorInd: mapSelectorInd === undefined ? null : mapSelectorInd,
    selectorGroups: mapSelectorGroups === undefined ? null : mapSelectorGroups,
    map: mapElement === undefined ? null : mapElement,
  }
  var mapModules = {
    locationCluster: LocationCluster,
    locationClusters: LocationClusters,
    marker: Marker,
    profile: Profile,
  }
  var externalModules = {
    google: window.google,
    markerClusterer: MarkerClusterer
  }
  return {mapModules, externalModules, htmlElements}
}
