var minClusterZoom = 14;

function mapSetup(queryStringMap, map_locations) {
  var selected_map;
  if (queryStringMap !== 'individuals') {
    selected_map = 'groups';
    renderMap(selected_map, map_locations.groups);
  } else {
    selected_map = 'individuals';
    renderMap(selected_map, map_locations.profiles, map_locations.private_profiles);
  }
  mapToggle(selected_map, map_locations);
}

function mapToggle(selected_map, map_locations) {
  var mapSelectorInd = document.getElementById('map_selector_ind')
  mapSelectorInd.onclick = function() {
    renderMap(selected_map, map_locations.profiles, map_locations.private_profiles);
  };
  var mapSelectorGroups = document.getElementById('map_selector_groups')
  mapSelectorGroups.onclick = function() {
    renderMap(map_locations.groups);
  }

  if (selected_map == "individuals") {
    mapSelectorInd.checked = true
  } else {
    mapSelectorGroups.checked = true
  }
}

function renderMap(selected_map, profiles, private_profiles) {
  var map = createMap();
  var locationClusters = createLocationClusters(profiles, selected_map)
  var markers = addMarkersWithLists(locationClusters, map, private_profiles);
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

function createLocationClusters(locations, profile_type) {
  var location_clusters = [];
  for (var i=0; i<locations.length; i++) {
    var location = locations[i];
    var j = 0;
    while (j < location_clusters.length) {
      var location_cluster = location_clusters[j]
      if (isSameLocation(location, location_cluster)) {
        var profile = {
          label: location.label,
          path: location.path
        }
        if (profile_type == 'groups') {
          profile.active = location.active
        }
        location_cluster.profiles.push(profile)
        break
      } else {
        j++
      }
    }
    if (isinSameLocationAsOneOf(location_clusters, j) == false) {
      new_location_cluster = createLocationCluster(location, profile_type)
      location_clusters.push(new_location_cluster)
    }
  }
  return location_clusters;
}

function isSameLocation(location, location_cluster) {
  return (location.lat == location_cluster.lat && location.lng == location_cluster.lng)
}

function isinSameLocationAsOneOf(location_clusters, j) {
  return (j < location_clusters.length)
}

function createLocationCluster(location,profile_type) {
  var cluster = {
    lat: location.lat,
    lng: location.lng,
    profiles: [{
      label: location.label,
      path: location.path,
    }]
  }
  if (profile_type == 'groups') {
    cluster.profiles[0].active = location.active;
  }
  return cluster;
}

function addMarkersWithLists(locationClusters, map, private_profiles) {
  var markers = [];
  for (var i=0; i< locationClusters.length; i++) {
      var locationCluster = locationClusters[i]
      var location = {lat: locationCluster.lat, lng: locationCluster.lng}
      var profiles = locationCluster.profiles
      var marker = createMarker(location)
      addDescription(marker, profiles)
      addLabel(marker, map)
      marker.setMap(map);
      markers.push(marker);
      var profiles_at_location = (private_profiles) ? profiles.length + count(private_profiles, location) : profiles.length
      addDummyMarkers(location, profiles_at_location, markers, map)
  }
  return markers
}

function addDescription(marker,profiles) {
  if (profiles.length > 1) {
    marker.desc = '<div class="map-label">'
    profiles.map(function(profile) {
      console.log(profile)
      marker.desc += "<a style='display: block' href='" + profile.path + "'>" + profile.label;
      marker.desc += (profile.active == "False") ? " (inactive)</a>" : "</a>"
    })
    marker.desc += '</div>'
  } else {
    marker.desc = "<a href='" + profiles[0].path + "'>" + profiles[0].label + "</a>";
  }
}

function addLabel(marker, map) {
  var iw = new google.maps.InfoWindow();
  marker.addListener('click', function() {
    iw.setContent(marker.desc);
    iw.open(map, marker);
  });
}

function createMarker(location,z=1) {
  var marker = new google.maps.Marker({
      position: location,
      optimized: !isIE,  // makes SVG icons work in IE
      zIndex: z
  });
  var iconSize = new google.maps.Size(20, 23);
  marker.setIcon({
   url: (location.active == "False") ? '/static/images/marker_inactive.svg' : '/static/images/marker_active.svg',
   size: iconSize,
   scaledSize: iconSize  // makes SVG icons work in IE
  });
  return marker
}

function count(private_profiles, location) {
  private_profiles_at_location = private_profiles.filter(function(private_profile) {
    return (private_profile.lat == location.lat) && (private_profile.lon == location.lon)
  })
  if (private_profiles_at_location.length > 0) {
    return private_profiles_at_location[0].count
  } else {
    return 0
  }
}

function addDummyMarkers(location, profiles_at_location, markers, map) {
  for (var i = 1; i < profiles_at_location; i++) {
    var dummyMarker = createMarker(location, z=1-i)
    dummyMarker.setMap(map);
    markers.push(dummyMarker)
  }
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
