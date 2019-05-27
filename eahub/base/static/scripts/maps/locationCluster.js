class LocationCluster {
  constructor(location, map) {
    this.location = {lat: location.lat, lng: location.lng}
    this.map = map
    this.profiles = []
    this.markers = []
  }

  addProfile(location) {
    var newProfile = new this.map.mapModules.profile(this.location, this.map.type)
    this.profiles.push(newProfile)
  }

  addMarker() {
    var newMarker = new this.map.mapModules.marker(this.map, this.location, this.profiles)
    this.markers.push(newMarker)
  }

  addDummyMarkers(z) {
    for (var i = 1; i < this.profiles.length; i++) {
      var z = 1-i
      var dummyMarker = new this.map.mapModules.marker(this.map, this.location, this.profiles, z)
      dummyMarker.googleMarker.setMap();
      this.markers.push(dummyMarker)
    }
  }

  isSameLocation(location) {
    return (location.lat == this.location.lat && location.lng == this.location.lng)
  }
}
