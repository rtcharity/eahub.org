var map = class {
  constructor(queryStringMap, locations, selectorInd, selectorGroups, google, markerClusterer, document, isIE, profileClass) {
    this.minClusterZoom = 14;
    this.type = queryStringMap
    this.locations = locations
    this.selectorInd = selectorInd
    this.selectorGroups = selectorGroups
    this.google = google
    this.markerClusterer = markerClusterer
    this.element = document.getElementById('map');
    this.isIE = isIE
    this.profileClass = profileClass
  }

  setup() {
    if (this.type !== 'individuals') {
      this.render(this.locations.groups);
      this.selectorGroups.checked = true
    } else {
      this.render(this.locations.profiles, this.locations.private_profiles);
      this.selectorInd.checked = true
    }
    this.toggle();
  }

  toggle() {
    this.selectorInd.onclick = function() {
      this.type = 'individuals'
      this.render(this.locations.profiles, this.locations.private_profiles);
    };
    this.selectorGroups.onclick = function() {
      this.type = 'groups'
      this.render(this.locations.groups);
    }
  }

  render(publicLocations, privateProfiles) {
    var map = this.createMap();
    var allLocations = (this.type == 'groups') ? publicLocations : publicLocations.concat(this.splitIntoIndividual(privateProfiles));
    var locationClusters = this.createLocationClusters(allLocations);
    var markers = this.addMarkersWithLists(locationClusters, map);
    this.createMarkerClusters(map, markers);
  }

  createMap() {
    var mapOptions = {
        zoom: 2,
        maxZoom: this.minClusterZoom+1,
        center: new this.google.maps.LatLng(30, 30), // roughly center of world (makes for better view than 0,0)
        typeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,

        // Snazzy map: pale
        styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#6195a0"}]},{"featureType":"administrative.province","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"lightness":"0"},{"saturation":"0"},{"color":"#f5f5f2"},{"gamma":"1"}]},{"featureType":"landscape.man_made","elementType":"all","stylers":[{"lightness":"-3"},{"gamma":"1.00"}]},{"featureType":"landscape.natural.terrain","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#bae5ce"},{"visibility":"on"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#fac9a9"},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"labels.text","stylers":[{"color":"#4e4e4e"}]},{"featureType":"road.arterial","elementType":"labels.text.fill","stylers":[{"color":"#787878"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.station.airport","elementType":"labels.icon","stylers":[{"hue":"#0a00ff"},{"saturation":"-77"},{"gamma":"0.57"},{"lightness":"0"}]},{"featureType":"transit.station.rail","elementType":"labels.text.fill","stylers":[{"color":"#43321e"}]},{"featureType":"transit.station.rail","elementType":"labels.icon","stylers":[{"hue":"#ff6c00"},{"lightness":"4"},{"gamma":"0.75"},{"saturation":"-68"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#eaf6f8"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"color":"#c7eced"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"lightness":"-49"},{"saturation":"-53"},{"gamma":"0.79"}]}]
    };

    var map = new this.google.maps.Map(this.element, mapOptions);
    return map
  }

  splitIntoIndividual(privateProfiles) {
    var individualPrivateProfiles = []
    privateProfiles.forEach(function(privateProfile) {
      for (var i=0; i<privateProfile.count; i++) {
        individualPrivateProfiles.push(privateProfile)
      }
    })
    return individualPrivateProfiles;
  }

  createLocationClusters(allLocations) {
    var locationClusters = [];
    for (var i=0; i<allLocations.length; i++) {
      var location = allLocations[i];
      var j = 0;
      while (j < locationClusters.length) {
        var locationCluster = locationClusters[j]
        if (this.isSameLocation(location, locationCluster)) {
          var profile = new this.profileClass(location, this.type)
          locationCluster.profiles.push(profile)
          break
        } else {
          j++
        }
      }
      if (this.isinSameLocationAsOneOf(locationClusters, j) == false) {
        var newLocationCluster = this.createLocationCluster(location)
        locationClusters.push(newLocationCluster)
      }
    }
    return locationClusters;
  }

  isSameLocation(location, locationCluster) {
    console.log(location.lat, locationCluster.lat)
    return (location.lat == locationCluster.lat && location.lng == locationCluster.lng)
  }

  isinSameLocationAsOneOf(locationClusters, j) {
    return (j < locationClusters.length)
  }

  createLocationCluster(location) {
    var cluster = {
      lat: location.lat,
      lng: location.lng,
    }
    var profile = new this.profileClass(location, this.type)
    cluster.profiles = [profile]
    return cluster;
  }

  addMarkersWithLists(locationClusters, map) {
    var markers = [];
    for (var i=0; i< locationClusters.length; i++) {
        var locationCluster = locationClusters[i]
        var location = {lat: locationCluster.lat, lng: locationCluster.lng}
        var profiles = locationCluster.profiles
        var marker = this.createMarker(location, locationClusters)
        this.addDescription(marker, profiles)
        this.addLabel(marker, map)
        marker.setMap(map);
        markers.push(marker);
        var profilesAtLocation = profiles.length;
        this.addDummyMarkers(location, profilesAtLocation, markers, map, locationClusters)
    }
    return markers
  }

  addDescription(marker, profiles) {
    var publicProfiles = profiles.filter(profile => !profile.anonymous)
    var privateProfiles = profiles.filter(profile => profile.anonymous)
    var allProfilesCount = publicProfiles.length + privateProfiles.length
    if (allProfilesCount > 1) {
      marker.desc = '<ul class="map-label">'
      publicProfiles.map(function(profile) {
        marker.desc += "<li><a style='display: block' href='" + profile.path + "'>" + profile.label;
        marker.desc += (profile.active == "False") ? " (inactive)</a></li>" : "</a></li>"
      })
      if (privateProfiles.length > 0) {
        userWord = (privateProfiles.length == 1) ? 'user' : 'users'
        marker.desc += '<li>' + privateProfiles.length.toString() + ' anonymous ' + userWord + '</li>'
      }
      marker.desc += '</ul>'
    } else if (!this.exists(publicProfiles) && this.exists(privateProfiles)) {
      var userWord = (privateProfiles.length == 1) ? 'user' : 'users'
      marker.desc = privateProfiles.length.toString() + ' anonymous ' + userWord
    } else if (publicProfiles.length == 1 && !exists(privateProfiles)) {
      marker.desc = "<a href='" + publicProfiles[0].path + "'>" + publicProfiles[0].label + "</a>";
    } else if (!this.exists(publicProfiles) && !this.exists(privateProfiles)) {
      return false;
    }
  }

  exists(profilesArray) {
    return (profilesArray.length > 0) ? true : false;
  }

  addLabel(marker, map) {
    var iw = new this.google.maps.InfoWindow();
    marker.addListener('click', function() {
      iw.setContent(marker.desc);
      iw.open(map, marker);
    });
  }

  createMarker(location, locationClusters, z=1) {
    var marker = new this.google.maps.Marker({
        position: location,
        label: {text: this.countMarkersAt(location, locationClusters).toString(), color: 'white', fontSize: '11px'},
        optimized: !this.isIE,  // makes SVG icons work in IE
        zIndex: z
    });

    var iconSize = new this.google.maps.Size(40, 40);
    marker.setIcon({
     url: (location.active == "False") ? '/static/images/marker_inactive.svg' : '/static/images/marker_active.svg',
     size: iconSize,
     scaledSize: iconSize  // makes SVG icons work in IE
    });
    return marker
  }

  countMarkersAt(location, locationClusters) {
    var clusterAtLocation = locationClusters.filter(cluster => this.isSameLocation(location, cluster))
    return clusterAtLocation[0].profiles.length
  }

  addDummyMarkers(location, profilesAtLocation, markers, map, locationClusters) {
    for (var i = 1; i < profilesAtLocation; i++) {
      var dummyMarker = this.createMarker(location, locationClusters, z=1-i)
      dummyMarker.setMap(map);
      markers.push(dummyMarker)
    }
  }

  createMarkerClusters(map, markers) {
    var markerCluster = new this.markerClusterer(
        map, markers,{imagePath: '../static/images/cluster/m', maxZoom: this.minClusterZoom}
    );

    this.google.maps.event.addListener(markerCluster, 'clusterclick', function(cluster) {
      map.fitBounds(cluster.getBounds());
      if( map.getZoom() > minClusterZoom+1 ) {
        map.setZoom(minClusterZoom+1);
      }
    });
  }
}

var mapObj = function() {
  return map
}()
