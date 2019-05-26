class LocationCluster {
  constructor(location, map) {
    this.location = {lat: location.lat, lng: location.lng}
    this.type = map.type
    this.profileClass = map.mapModules.profile
    this.markerClass = map.mapModules.marker
    this.google = map.google
    this.googleMap = map.googleMap
    this.isIE = map.isIE
    this.profiles = []
    this.markers = []
    this.size = this.profiles.length
  }

  addProfile(location) {
    var newProfile = new this.profileClass(location, this.type)
    this.profiles.push(newProfile)
  }

  addMarker() {
    var newMarker = new this.markerClass(this.isIE, this.google, this.googleMap, this.location, this.profiles)
    this.markers.push(newMarker)
  }

  addDummyMarkers(z) {
    for (var i = 1; i < this.profiles.length; i++) {
      var z = 1-i
      var dummyMarker = new this.markerClass(this.isIE, this.google, this.googleMap, this.location, this.profiles, z)
      dummyMarker.googleMarker.setMap();
      this.markers.push(dummyMarker)
    }
  }

  isSameLocation(location) {
    return (location.lat == this.location.lat && location.lng == this.location.lng)
  }
}

export { LocationCluster }
