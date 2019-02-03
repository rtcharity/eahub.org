var minClusterZoom = 14;

function mapSetup(queryStringMap, mapDataProfiles, mapDataGroups) {
  mapToggle(queryStringMap, mapDataProfiles, mapDataGroups)

  //call renderMap when page loads
  renderMap(queryStringMap, mapDataProfiles, mapDataGroups);
}

function mapToggle(queryStringMap, mapDataProfiles, mapDataGroups) {
  console.log(queryStringMap)
  var selectedMap;

  var mapSelectorInd = document.getElementById('map_selector_ind')
  mapSelectorInd.onclick = function() {
    selectedMap = 'individuals';
    renderMap(selectedMap, mapDataProfiles, mapDataGroups);
  };
  var mapSelectorGroups = document.getElementById('map_selector_groups')
  mapSelectorGroups.onclick = function() {
    selectedMap = 'groups';
    renderMap(selectedMap, mapDataProfiles, mapDataGroups);
  }

  if (queryStringMap == "groups") {
    mapSelectorGroups.checked = true
  } else {
    mapSelectorInd.checked = true
  }
}

function renderMap(selectedMap, mapDataProfiles, mapDataGroups) {
  if (selectedMap !== 'individuals' && selectedMap !== 'groups') {
    selectedMap = 'individuals'
  }
  var locations = selectedMap == 'individuals' ? mapDataProfiles : mapDataGroups
  if (selectedMap == 'individuals') {
    renderProfileMap(locations)
  } else {
    renderGroupMap(locations)
  }
}

function renderProfileMap(locations) {
  var map = createMap();
  var markers = addMarkersWithLabelsGDPRUnlocked(locations, map);
  createMarkerClusters(map, markers);
}

function renderGroupMap(locations) {
  var map = createMap();
  var markers = addMarkersWithLabels(locations, map);
  createMarkerClusters(map, markers);
}

function createMap() {
  var mapOptions = {
      zoom: 2,
      maxZoom: minClusterZoom+1,
      center: new google.maps.LatLng(30, 30), // roughly center of world (makes for better view than 0,0)
      mapTypeControl: false,
      scaleControl: false,
      streetViewControl: false,
      rotateControl: false,

      // Snazzy map: pale
      styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#6195a0"}]},{"featureType":"administrative.province","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"lightness":"0"},{"saturation":"0"},{"color":"#f5f5f2"},{"gamma":"1"}]},{"featureType":"landscape.man_made","elementType":"all","stylers":[{"lightness":"-3"},{"gamma":"1.00"}]},{"featureType":"landscape.natural.terrain","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#bae5ce"},{"visibility":"on"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#fac9a9"},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"labels.text","stylers":[{"color":"#4e4e4e"}]},{"featureType":"road.arterial","elementType":"labels.text.fill","stylers":[{"color":"#787878"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.station.airport","elementType":"labels.icon","stylers":[{"hue":"#0a00ff"},{"saturation":"-77"},{"gamma":"0.57"},{"lightness":"0"}]},{"featureType":"transit.station.rail","elementType":"labels.text.fill","stylers":[{"color":"#43321e"}]},{"featureType":"transit.station.rail","elementType":"labels.icon","stylers":[{"hue":"#ff6c00"},{"lightness":"4"},{"gamma":"0.75"},{"saturation":"-68"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#eaf6f8"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"color":"#c7eced"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"lightness":"-49"},{"saturation":"-53"},{"gamma":"0.79"}]}]
  };

  var mapElement = document.getElementById('map');
  var map = new google.maps.Map(mapElement, mapOptions);
  return map
}

function addMarkersWithLabels(locations, map) {
  var iw = new google.maps.InfoWindow();

  //oms allows for spiderfying of clusters
  var oms = new OverlappingMarkerSpiderfier(map, {
    markersWontMove: true,
    markersWontHide: true,
    basicFormatEvents: true
  });

  oms.addListener('click', function(marker) {
    iw.setContent(marker.desc);
    iw.open(map, marker);
  });

  var markers = locations.map(function(location, i) {
      var marker = new google.maps.Marker({
          position: location,
          optimized: !isIE  // makes SVG icons work in IE
      });
      var iconSize = new google.maps.Size(20, 23);
      marker.setIcon({
       url: '/static/images/marker.svg',
       size: iconSize,
       scaledSize: iconSize  // makes SVG icons work in IE
      });

      var label = location.label.toLowerCase()
        .split(' ')
        .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
        .join(' ');
      marker.desc = "<a href='" + location.path + "'>" + label + "</a>";
      oms.addMarker(marker);
      return marker;
  });
  return markers
}

function addMarkersWithoutLables(locations, map) {
  var markers = locations.map(function(location, i) {
      var marker = new google.maps.Marker({
          position: location,
          map: map,
          optimized: !isIE  // makes SVG icons work in IE
      });
      var iconSize = new google.maps.Size(20, 23);
      marker.setIcon({
       url: '/static/images/marker.svg',
       size: iconSize,
       scaledSize: iconSize  // makes SVG icons work in IE
      });
      return marker;
  });
  return markers
}

function addMarkersWithLabelsGDPRUnlocked(locations, map) {
  var iw = new google.maps.InfoWindow();

  //oms allows for spiderfying of clusters
  var oms = new OverlappingMarkerSpiderfier(map, {
    markersWontMove: true,
    markersWontHide: true,
    basicFormatEvents: true
  });

  oms.addListener('click', function(marker) {
    if (marker.gdpr_confirmed) {
      iw.setContent(marker.desc);
      iw.open(map, marker);
    }
  });

  var markers = locations.map(function(location, i) {
      var marker = new google.maps.Marker({
          position: location,
          optimized: !isIE  // makes SVG icons work in IE
      });
      var iconSize = new google.maps.Size(20, 23);
      marker.setIcon({
       url: '/static/images/marker.svg',
       size: iconSize,
       scaledSize: iconSize  // makes SVG icons work in IE
      });
      if (location.gdpr_confirmed == 'True') {
        var label = location.label.toLowerCase()
          .split(' ')
          .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
          .join(' ');
        marker.desc = "<a href='" + location.path + "'>" + label + "</a>";
        marker.gdpr_confirmed = true
      } else {
        marker.gdpr_confirmed = false
      }
      oms.addMarker(marker);
      return marker;
  });
  return markers
}

function createMarkerClusters(map, markers) {
  var markerCluster = new MarkerClusterer(
      map, markers,{imagePath: '../static/images/cluster/m', maxZoom: minClusterZoom}
  );

  google.maps.event.addListener(markerCluster, 'clusterclick', function(cluster) {
    map.fitBounds(cluster.getBounds());
    if( map.getZoom() > minClusterZoom+1 ) {
      map.setZoom(minClusterZoom+1);
    }
  });
}
