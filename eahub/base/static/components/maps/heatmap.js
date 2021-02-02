const MARKERSETTINGS = {
  image: {
    active: '/static/global/images/marker_active.svg',
    inactive: '/static/global/images/marker_inactive.svg'
  },
  size: {
    fullmap: { width: 40, height: 40 },
    profilemap: { width: 20, height: 23 }
  }
}

export default class Heatmap {
  constructor(queryStringMap, locations, mapModules, externalModules, htmlElements, isIE) {
    this.minClusterZoom = 14;
    this.type = (queryStringMap !== 'groups') ? 'individuals' : 'groups';
    this.locations = locations;
    this.mapModules = mapModules;
    this.selectorInd = htmlElements.selectorInd;
    this.selectorGroups = htmlElements.selectorGroups;
    this.element = htmlElements.map;
    this.locationClusters = null;
    this.google = externalModules.google;
    this.markerClusterer = externalModules.markerClusterer
    this.isIE = isIE;
    this.googleMap = null;
    this.markerSettings = MARKERSETTINGS;
  }

  setup() {
    if (this.type === 'individuals') {
      this.render(this.locations.profiles, this.locations.private_profiles);
      this.selectorInd.checked = true;
    }
    if (this.type === 'groups') {
      this.render(this.locations.groups);
      this.selectorGroups.checked = true;
    }
    this.toggle();
  }

  toggle() {
    var that = this
    that.selectorInd.onclick = function() {
      that.type = 'individuals'
      that.render(that.locations.profiles, that.locations.private_profiles);
    };
    that.selectorGroups.onclick = function() {
      that.type = 'groups'
      that.render(that.locations.groups);
    }
  }

  render(publicLocations, privateProfiles) {
    this.googleMap = this.createMap();
    var allLocations = (privateProfiles === undefined) ? publicLocations : publicLocations.concat(this.splitIntoIndividual(privateProfiles));
    this.locationClusters = new this.mapModules.locationClusters(allLocations, this);
    this.addMarkersWithLists();
    this.createMarkerClusters();
  }

  renderProfilePageMap() {
    var profileLocations = this.locations.profiles[0]
    var mapOptions = {
        zoom: 3,
        center: new this.google.maps.LatLng(profileLocations.lat, profileLocations.lng),
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        gestureHandling: 'none',
        zoomControl: false,
        fullscreenControl: false,
        // Snazzy map: pale
        styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#6195a0"}]},{"featureType":"administrative.province","elementType":"geometry.stroke","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"lightness":"0"},{"saturation":"0"},{"color":"#f5f5f2"},{"gamma":"1"}]},{"featureType":"landscape.man_made","elementType":"all","stylers":[{"lightness":"-3"},{"gamma":"1.00"}]},{"featureType":"landscape.natural.terrain","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"geometry.fill","stylers":[{"color":"#bae5ce"},{"visibility":"on"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#fac9a9"},{"visibility":"simplified"}]},{"featureType":"road.highway","elementType":"labels.text","stylers":[{"color":"#4e4e4e"}]},{"featureType":"road.arterial","elementType":"labels.text.fill","stylers":[{"color":"#787878"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.station.airport","elementType":"labels.icon","stylers":[{"hue":"#0a00ff"},{"saturation":"-77"},{"gamma":"0.57"},{"lightness":"0"}]},{"featureType":"transit.station.rail","elementType":"labels.text.fill","stylers":[{"color":"#43321e"}]},{"featureType":"transit.station.rail","elementType":"labels.icon","stylers":[{"hue":"#ff6c00"},{"lightness":"4"},{"gamma":"0.75"},{"saturation":"-68"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#eaf6f8"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"color":"#c7eced"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"lightness":"-49"},{"saturation":"-53"},{"gamma":"0.79"}]}]
    };


      var map = new this.google.maps.Map(this.element, mapOptions);
      var marker = new this.google.maps.Marker({
          position: {lat: profileLocations.lat, lng: profileLocations.lng},
          map: map,
          optimized: !this.isIE  // makes SVG icons work in IE
      });
      var iconSize = new google.maps.Size(this.markerSettings.size.profilemap.width, this.markerSettings.size.profilemap.height);
      marker.setIcon({
       url: profileLocations.active ? this.markerSettings.image.inactive : this.markerSettings.image.active,
       size: iconSize,
       scaledSize: iconSize  // makes SVG icons work in IE
      });
    }

  createMap() {
    var mapOptions = {
        zoom: 2,
        maxZoom: this.minClusterZoom+1,
        center: new this.google.maps.LatLng(30, 30), // roughly center of world (makes for better view than 0,0)
        typeControl: false,
        scaleControl: false,
        streetViewControl: false,
        mapTypeControl: false,
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

  addMarkersWithLists() {
    for (var i=0; i< this.locationClusters.list.length; i++) {
        var locationCluster = this.locationClusters.list[i]
        locationCluster.addMarker()
        var marker = locationCluster.markers[0]
        marker.addDescription()
        marker.addLabel()
        marker.googleMarker.setMap(this.googleMap);
        locationCluster.addDummyMarkers()
    }
  }

  createMarkerClusters() {
    let map = this.googleMap
    let markers = this.locationClusters.getGoogleMarkers()
    var markerCluster = new this.markerClusterer(
        map, markers, {imagePath: '../static/global/images/cluster/m', maxZoom: this.minClusterZoom}
    );

    this.google.maps.event.addListener(markerCluster, 'clusterclick', function(cluster) {
      map.fitBounds(cluster.getBounds());
      if( map.getZoom() > minClusterZoom+1 ) {
        map.setZoom(minClusterZoom+1);
      }
    });
  }
}
