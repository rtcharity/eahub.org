var minClusterZoom = 14;
var mapSelectorInd = document.getElementById('map_selector_ind');
var mapSelectorGroups = document.getElementById('map_selector_groups');

function mapSetup(queryStringMap, map_locations) {
  var map_type;
  if (queryStringMap !== 'individuals') {
    renderMap('groups', map_locations.groups);
    mapSelectorGroups.checked = true
  } else {
    renderMap('individuals', map_locations.profiles, map_locations.private_profiles);
    mapSelectorInd.checked = true
  }
  mapToggle(map_locations);
}

function mapToggle(map_locations) {
  mapSelectorInd.onclick = function() {
    renderMap('individuals', map_locations.profiles, map_locations.private_profiles);
  };
  mapSelectorGroups.onclick = function() {
    renderMap('groups', map_locations.groups);
  }
}

function renderMap(map_type, public_locations, private_profiles) {
  var map = createMap();
  var all_locations = (private_profiles == undefined) ? public_locations : public_locations.concat(splitIntoIndividual(private_profiles));
  var location_clusters = createLocationClusters(map_type, all_locations);
  var markers = addMarkersWithLists(location_clusters, map);
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

function splitIntoIndividual(private_profiles) {
  individual_private_profiles = []
  private_profiles.forEach(function(private_profile) {
    for (var i=0; i<private_profile.count; i++) {
      individual_private_profiles.push(private_profile)
    }
  })
  return individual_private_profiles;
}

function createLocationClusters(map_type, all_locations) {
  var location_clusters = [];
  for (var i=0; i<all_locations.length; i++) {
    var location = all_locations[i];
    var j = 0;
    while (j < location_clusters.length) {
      var location_cluster = location_clusters[j]
      if (isSameLocation(location, location_cluster)) {
        var profile = createProfile(map_type, location)
        location_cluster.profiles.push(profile)
        break
      } else {
        j++
      }
    }
    if (isinSameLocationAsOneOf(location_clusters, j) == false) {
      new_location_cluster = createLocationCluster(map_type, location)
      location_clusters.push(new_location_cluster)
    }
  }
  return location_clusters;
}

function createProfile(map_type, location) {
  var profile = {}
  if (location.label != undefined) {
    profile.label = location.label
  } else {
    profile.anonymous = true
  }
  if (location.path != undefined) profile.path = location.path
  if (map_type == 'groups') {
    profile.active = location.active
  }
  return profile;
}

function isSameLocation(location, location_cluster) {
  return (location.lat == location_cluster.lat && location.lng == location_cluster.lng)
}

function isinSameLocationAsOneOf(location_clusters, j) {
  return (j < location_clusters.length)
}

function createLocationCluster(map_type, location) {
  var cluster = {
    lat: location.lat,
    lng: location.lng,
  }
  var profile = createProfile(map_type, location)
  cluster.profiles = [profile]
  return cluster;
}

function addMarkersWithLists(location_clusters, map) {
  var markers = [];
  for (var i=0; i< location_clusters.length; i++) {
      var location_cluster = location_clusters[i]
      var location = {lat: location_cluster.lat, lng: location_cluster.lng}
      var profiles = location_cluster.profiles
      var marker = createMarker(location, location_clusters)
      addDescription(marker, profiles)
      addLabel(marker, map)
      marker.setMap(map);
      markers.push(marker);
      var profiles_at_location = profiles.length;
      addDummyMarkers(location, profiles_at_location, markers, map, location_clusters)
  }
  return markers
}

function addDescription(marker, profiles) {
  public_profiles = profiles.filter(profile => !profile.anonymous)
  private_profiles = profiles.filter(profile => profile.anonymous)
  if (public_profiles.length > 1) {
    marker.desc = '<ul class="map-label">'
    public_profiles.map(function(profile) {
      marker.desc += "<li><a style='display: block' href='" + profile.path + "'>" + profile.label;
      marker.desc += (profile.active == "False") ? " (inactive)</a></li>" : "</a></li>"
    })
    if (private_profiles.length > 0) {
      user_word = (private_profiles.length == 1) ? 'user' : 'users'
      marker.desc += '<li>' + private_profiles.length.toString() + ' anonymous ' + user_word + '</li>'
    }
    marker.desc += '</ul>'
  } else if (public_profiles.length == 1) {
    marker.desc = "<a href='" + public_profiles[0].path + "'>" + public_profiles[0].label + "</a>";
  } else {
    marker.desc = "All users at this location are anonymous";
  }
}

function addLabel(marker, map) {
  var iw = new google.maps.InfoWindow();
  marker.addListener('click', function() {
    iw.setContent(marker.desc);
    iw.open(map, marker);
  });
}

function createMarker(location, location_clusters, z=1) {
  var marker = new google.maps.Marker({
      position: location,
      label: {text: countMarkersAt(location, location_clusters).toString(), color: 'white', fontSize: '11px'},
      optimized: !isIE,  // makes SVG icons work in IE
      zIndex: z
  });

  var iconSize = new google.maps.Size(40, 40);
  marker.setIcon({
   url: (location.active == "False") ? '/static/images/marker_inactive.svg' : '/static/images/marker_active.svg',
   size: iconSize,
   scaledSize: iconSize  // makes SVG icons work in IE
  });
  return marker
}

function countMarkersAt(location, location_clusters) {
  cluster_at_location = location_clusters.filter(cluster => isSameLocation(location, cluster))
  return cluster_at_location[0].profiles.length
}

function addDummyMarkers(location, profiles_at_location, markers, map, location_clusters) {
  for (var i = 1; i < profiles_at_location; i++) {
    var dummyMarker = createMarker(location, location_clusters, z=1-i)
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
