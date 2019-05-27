class Marker {
  constructor(map, location, profiles, z=1) {
    this.google = map.google
    this.googleMap = map.googleMap
    this.location = location
    this.clusterSize = profiles.length
    this.clusterProfiles = profiles
    this.clusterType = map.type
    this.googleMarker = this.create(map.isIE, z)
  }

  create(isIE, z) {
    var googleMarker = new this.google.maps.Marker({
        position: this.location,
        label: {text: this.clusterSize.toString(), color: 'white', fontSize: '11px'},
        optimized: !isIE,  // makes SVG icons work in IE
        zIndex: z
    });

    var iconSize = new this.google.maps.Size(40, 40);
    var inactiveSingleProfile = this.clusterType == 'groups' && this.clusterProfiles.every(function(profile) { return profile.active === 'False' } )
    googleMarker.setIcon({
     url: (inactiveSingleProfile) ? '/static/images/marker_inactive.svg' : '/static/images/marker_active.svg',
     size: iconSize,
     scaledSize: iconSize  // makes SVG icons work in IE
    });
    return googleMarker
  }

  addDescription() {
      var publicProfiles = this.clusterProfiles.filter(profile => !profile.anonymous)
      var privateProfiles = this.clusterProfiles.filter(profile => profile.anonymous)
      var allProfilesCount = publicProfiles.length + privateProfiles.length
      var googleMarker = this.googleMarker
      var that = this
      if (allProfilesCount > 1) {
        googleMarker.desc = '<ul class="map-label">'
        publicProfiles.map(function(profile) {
          googleMarker.desc += "<li><a style='display: block' href='" + profile.path + "'>" + profile.label;
          googleMarker.desc += (profile.active == "False") ? " (inactive)</a></li>" : "</a></li>"
        })
        if (privateProfiles.length > 0) {
          userWord = (privateProfiles.length == 1) ? 'user' : 'users'
          googleMarker.desc += '<li>' + privateProfiles.length.toString() + ' anonymous ' + userWord + '</li>'
        }
        googleMarker.desc += '</ul>'
      } else if (that.exists(publicProfiles) && that.exists(privateProfiles)) {
        var userWord = (privateProfiles.length == 1) ? 'user' : 'users'
        googleMarker.desc = privateProfiles.length.toString() + ' anonymous ' + userWord
      } else if (publicProfiles.length == 1 && !that.exists(privateProfiles)) {
        googleMarker.desc = "<a href='" + publicProfiles[0].path + "'>" + publicProfiles[0].label + "</a>";
      } else if (!that.exists(publicProfiles) && !that.exists(privateProfiles)) {
        return false;
      }
  }

  addLabel() {
    var googleMarker = this.googleMarker
    var google = this.google
    var map = this.googleMap
    var iw = new google.maps.InfoWindow();
    googleMarker.addListener('click', function() {
      iw.setContent(googleMarker.desc);
      iw.open(map, googleMarker);
    });
  }

  exists(profilesArray) {
    return (profilesArray.length > 0) ? true : false;
  }
}
