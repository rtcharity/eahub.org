export default class LocationClusters {
  constructor(allLocations, map) {
    this.map = map
    this.list = this.create(allLocations)
    this.markers = this.getGoogleMarkers()
  }

  add(newCluster) {
    let that = this
    let i = 0
    while (i < that.list.length) {
      let cluster = that.list[i]
      if (cluster.isSameLocation(newCluster.location)) {
        that.list[i] = newCluster
        break
      } else {
        i++
      }
    }
    if (i == that.list.length) that.list.push(newCluster)
  }

  create(allLocations) {
    var list = []
    for (var i=0; i<allLocations.length; i++) {
      var location = allLocations[i];
      var j = 0;
      while (j < list.length) {
        var locationCluster = list[j]
        if (locationCluster.isSameLocation(location)) {
          locationCluster.addProfile(location)
          list[j] = locationCluster
          break
        } else {
          j++
        }
      }
      if (this.isinSameLocationAsOneOf(list, j) == false) {
        var locationClusterClass = this.map.mapModules.locationCluster
        var profileClass = this.map.mapModules.profile
        var profile = new profileClass(location, this.map.type)
        var newLocationCluster = new locationClusterClass(location, this.map)
        newLocationCluster.profiles = [profile]
        list.push(newLocationCluster)
      }
    }
    return list
  }

  getGoogleMarkers() {
    var markers = []
    this.list.forEach(function(cluster) {
      cluster.markers.forEach(function(marker) {
        markers.push(marker.googleMarker)
      })
    })
    return markers
  }

  isinSameLocationAsOneOf(list, j) {
    return (j < list.length)
  }
}
