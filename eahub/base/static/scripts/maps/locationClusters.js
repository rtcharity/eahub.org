class LocationClusters {
  constructor(allLocations, map) {
    this.map = map
    this.list = this.create(allLocations)
    this.markers = this.getMarkers()
  }

  add(newCluster) {
    this.list.forEach(function(cluster, i) {
      if (cluster.isSameLocation(cluster.location)) {
        this.list[i] = newCluster
      } else {
        this.list.push(newCluster)
      }
    })
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
        console.log(newLocationCluster)
        list.push(newLocationCluster)
      }
    }
    console.log(list)
    return list
  }

  getMarkers() {
    var markers = []
    this.list.forEach(function(cluster) {
      markers.push(cluster.markers.obj)
    })
    return markers
  }

  isinSameLocationAsOneOf(list, j) {
    return (j < list.length)
  }
}

export { LocationClusters }
