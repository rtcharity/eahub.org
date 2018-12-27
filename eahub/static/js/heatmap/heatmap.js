function map(selected_map, map_data_profiles, map_data_groups, page_name) {
  var selectedMap, mapDataProfiles, mapDataGroups;

  //Toggle between individual and groups map
  var mapSelectorInd = document.getElementById('map_selector_ind')
  mapSelectorInd.onclick = function() {
    selectedMap = 'individuals';
    renderMap(selectedMap);
  };
  var mapSelectorGroups = document.getElementById('map_selector_groups')
  mapSelectorGroups.onclick = function() {
    selectedMap = 'groups';
    renderMap(selectedMap);
  }
  if (page_name == 'Profiles') {
      mapSelectorInd.setAttribute("checked", "checked")
  } else {
      mapSelectorGroups.setAttribute("checked", "checked")
  }

  function renderMap(selectedMap = selected_map, mapDataProfiles = map_data_profiles, mapDataGroups = map_data_groups, pageName = page_name) {
    //checks whether to render groups or individuals
    if (selectedMap == null) {
      selectedMap = pageName == 'Profiles' ? 'individuals' : 'groups'
    }
    var locations = selectedMap == 'individuals' ? mapDataProfiles : mapDataGroups

    var minClusterZoom = 14;
    var mapOptions = {
        zoom: 1.6,
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
          console.log(location);
          var marker = new google.maps.Marker({
              position: location,
              optimized: !isIE  // makes SVG icons work in IE
          });
          var iconSize = new google.maps.Size(20, 23);
          marker.setIcon({
           url: '/static/imgs/marker.svg',
           size: iconSize,
           scaledSize: iconSize  // makes SVG icons work in IE
          });
          marker.desc = "<a href='" + location.path + "'>" + location.label + "</a>";
          oms.addMarker(marker);
          return marker;
      });

      // Add a marker clusterer to manage the markers.
      var markerCluster = new MarkerClusterer(
          map, markers,{imagePath: '../static/imgs/cluster/m', maxZoom: minClusterZoom}
      );
      // prevent map from zooming in too much when clicking on cluster
      google.maps.event.addListener(markerCluster, 'clusterclick', function(cluster) {
        map.fitBounds(cluster.getBounds());
        if( map.getZoom() > minClusterZoom+1 ) {
          map.setZoom(minClusterZoom+1);
        }
      });
  }

  //call renderMap when page loads
  renderMap()
}
